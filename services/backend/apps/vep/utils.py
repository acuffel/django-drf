import logging
import subprocess
from pathlib import Path
from pydantic import ValidationError
from typing import Any, Generator

from vep.models import (
    VEP106BasicModel,
    VEP106FullModel,
)

logger = logging.getLogger(__name__)


def ping():
    """Returns 0 if Ensembl VEP works."""
    vep = subprocess.run(
        [
            "vep",
            "--help",
        ],
        capture_output=True,
        encoding="utf_8",
    )

    if vep.stdout:
        logger.info("stdout: %s", vep.stdout)
    if vep.stderr:
        logger.error("stderr: %s", vep.stderr)
    if vep.returncode:
        logger.error("returncode: %s", vep.returncode)

    return vep.returncode


def get_fields(
    dir_cache: Path = "/code/services/backend/biodb/ftp.ensembl.org/pub/release-106/variation/indexed_vep_cache",
    fasta: Path = "/code/services/backend/biodb/ftp.ensembl.org/pub/release-106/fasta/homo_sapiens/dna_index/Homo_sapiens.GRCh38.dna.toplevel.fa",
    variant: str = "3 46358464 . A AGAC",
    assembly: str = "GRCh38",
    options: list[str] = [],
    field_type: str = "basic",
) -> list[dict[str]]:
    if field_type == "full":
        options = ["--everything"]
    vep = subprocess.run(
        [
            "vep",
            "--cache",
            "--offline",
            "--no_stats",
            "--dir_cache",
            dir_cache,
            "--species",
            "homo_sapiens",
            "--assembly",
            assembly,
            "--fasta",
            fasta,
            "--merged",
            "--input_data",
            variant,
            "--output_file",
            "STDOUT",
            "--tab",
        ]
        + options,
        capture_output=True,
        encoding="utf_8",
    )

    if vep.stdout:
        logger.info(
            "stdout: %s", vep.stdout.replace("\n", " ").replace("\r", "") or "No data"
        )

    if vep.stderr or vep.returncode:
        logger.error(
            "stderr: %s",
            vep.stderr.replace("\n", " ").replace("\r", "") or "No data",
        )
        logger.error("returncode: %s", vep.returncode)
        raise Exception("An exception occurred while trying to parse vep result!")

    try:
        vep_list = vep.stdout.split("\n")
        vep_fields = []

        for row in filter(lambda row: (row[0:2] == "##" and " :" in row), vep_list):
            cleaned_row: str = row[3:].rstrip()
            vep_fields.append(cleaned_row.split(" :")[0])
        return vep_fields

    except Exception as e:
        logger.exception(e)
        raise Exception("An exception occurred while trying to parse vep result!")


def annotate_variant(
    dir_cache: Path = "/code/services/backend/biodb/ftp.ensembl.org/pub/release-106/variation/indexed_vep_cache",
    fasta: Path = "/code/services/backend/biodb/ftp.ensembl.org/pub/release-106/fasta/homo_sapiens/dna_index/Homo_sapiens.GRCh38.dna.toplevel.fa",
    variant: str = "3 46358464 . A AGAC",
    assembly: str = "GRCh38",
    fields: list[str] = ["Uploaded_variation", "Location", "Allele", "Gene", "Feature"],
    options: list[str] = ["--everything"],
) -> list[dict[str, Any]]:
    vep = subprocess.run(
        [
            "vep",
            "--cache",
            "--offline",
            "--no_stats",
            "--dir_cache",
            dir_cache,
            "--species",
            "homo_sapiens",
            "--assembly",
            assembly,
            "--fasta",
            fasta,
            "--merged",
            "--input_data",
            variant,
            "--output_file",
            "STDOUT",
            "--tab",
            "--no_headers",
            "--fields",
            ",".join(fields),
        ]
        + options,
        capture_output=True,
        encoding="utf_8",
    )

    if vep.stdout:
        logger.info(
            "stdout: %s", vep.stdout.replace("\n", " ").replace("\r", "") or "No data"
        )

    if vep.stderr or vep.returncode:
        logger.error(
            "stderr: %s",
            vep.stderr.replace("\n", " ").replace("\r", "") or "No data",
        )
        logger.error("returncode: %s", vep.returncode)
        raise Exception("An exception occurred while trying to parse vep result!")

    try:
        annotations = []
        lines = vep.stdout.split("\n")

        for line in lines:
            if line:
                values = line.split("\t")
                annotation = dict(zip(fields, values))
                annotations.append(annotation)

        return annotations

    except Exception as e:
        logger.exception(e)
        raise Exception("An exception occurred while trying to parse vep result!")


def annotate_vcf(
    dir_cache: Path,
    fasta: Path,
    vcf,
    assembly: str,
    field_type: str,
    fields: list[str],
    options: list[str] = ["--everything"],
) -> list[dict[str, Any]]:
    from annotations.models import Annotation

    vep = subprocess.run(
        [
            "vep",
            "-i",
            vcf,
            "--cache",
            "--no_stats",
            "--dir_cache",
            dir_cache,
            "--species",
            "homo_sapiens",
            "--assembly",
            assembly,
            "--fasta",
            fasta,
            "--merged",
            "--output_file",
            "STDOUT",
            "--tab",
            "--no_headers",
            "--no_check_variants_order",
            "--fields",
            ",".join(fields),
        ],
        capture_output=True,
        encoding="utf_8",
    )

    # if vep.stdout:
    #     logger.info(
    #         "stdout: %s", vep.stdout.replace("\n", " ").replace("\r", "") or "No data"
    #     )

    if vep.stderr or vep.returncode:
        logger.error(
            "stderr: %s",
            vep.stderr.replace("\n", " ").replace("\r", "") or "No data",
        )
        logger.error("returncode: %s", vep.returncode)
        raise Exception("An exception occurred while trying to parse vep result!")

    try:
        lines = vep.stdout.split("\n")
        for line in lines:
            if line:
                values = line.split("\t")
                if field_type == Annotation.FieldTypeChoices.BASIC:
                    try:
                        yield VEP106BasicModel(**dict(zip(fields, values)))

                    except ValidationError as e:
                        yield e
                else:
                    try:
                        yield VEP106FullModel(**dict(zip(fields, values)))

                    except ValidationError as e:
                        yield e

    except Exception as e:
        logger.exception(e)
        raise Exception("An exception occurred while trying to parse vep result!")


def get_annotations_vep(annotation_pk: int) -> Generator[None, None, None]:
    from annotations.models import Annotation

    fields = []
    annotation = Annotation.objects.get(pk=annotation_pk)

    if annotation.field_type == Annotation.FieldTypeChoices.BASIC:        
        fields = list(VEP106BasicModel.__fields__.keys())
    else:
        fields = list(VEP106FullModel.__fields__.keys())

    annotations_vep = annotate_vcf(
        dir_cache=annotation.get_indexed_vep_cache_path(),
        fasta=annotation.assembly.assessions.fasta_file.path,
        vcf=annotation.vcf_file.path,
        assembly=annotation.assembly_id,
        field_type=annotation.field_type,
        fields=fields,
    )
    
    return annotations_vep
