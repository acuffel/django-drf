from core.models import BaseModel
from django.utils.translation import gettext as _

# Warning
# Be aware when using mixins in StackedInline/TabularInline admin objects that an issue
# affects `get_fields()`, `get_readonly_fields()`, `get_fieldsets()`,
# `get_prepopulated_fields()`, etc.
# In those methods, `obj` is the parent object, not a child object from the inline.
# See: https://code.djangoproject.com/ticket/15602


class DefaultModelMixin(object):
    # Default values that can be overwritten in each child class:
    fields = None
    readonly_fields = ()
    readonly_fields_new = ()
    list_display = ()
    search_fields = ()
    list_filter = ()

    # Default values that can be overwritten in each child mixin:
    fieldsets_base = (
        (
            _("generic fields"),
            {
                # "classes": ("collapse",),
                "fields": ("id",),
            },
        ),
    )
    readonly_fields_base = ("id",)
    readonly_fields_new_base = ()
    list_display_base = ()
    search_fields_base = ()
    list_filter_base = ()

    def get_fieldsets(self, request, obj=None):
        if self.fields:
            return self.fieldsets_base + (
                (
                    _("specific fields"),
                    {
                        "fields": self.fields,
                    },
                ),
            )
        return self.fieldsets_base

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields_base + self.readonly_fields
        else:
            return (
                self.readonly_fields_base
                + self.readonly_fields
                + self.readonly_fields_new_base
                + self.readonly_fields_new
            )

    def get_list_display(self, request):
        return ("__str__",) + self.list_display + self.list_display_base

    def get_search_fields(self, request):
        return self.search_fields_base + self.search_fields

    def get_list_filter(self, request):
        return self.list_filter_base + self.list_filter

    def save_related(self, request, form, formsets, change):
        """Given the ``HttpRequest``, the parent ``ModelForm`` instance, the
        list of inline formsets and a boolean value based on whether the
        parent is being added or changed, save the related objects to the
        database. Note that at this point save_form() and save_model() have
        already been called.
        """

        for formset in formsets:
            if issubclass(formset.model, BaseModel):
                instances = formset.save(commit=False)

                for instance in instances:
                    instance.changed_by = request.user

                for added_obj in formset.new_objects:
                    added_obj.owner = request.user

                # for deleted_obj in formset.deleted_objects:
                #     pass

                # for changed_obj in formset.changed_objects:
                #     pass

        super(DefaultModelMixin, self).save_related(request, form, formsets, change)


class BaseModelMixin(DefaultModelMixin):
    fieldsets_base = (
        (
            _("generic fields"),
            {
                # "classes": ("collapse",),
                "fields": (
                    "id",
                    "owner",
                    "metadata",
                ),
            },
        ),
        (
            _("history fields"),
            {
                # "classes": ("collapse",),
                "fields": (
                    (
                        "created_at",
                        "changed_at",
                        "changed_by",
                    ),
                ),
            },
        ),
    )

    readonly_fields_base = (
        "id",
        # "owner",
        "created_at",
        "changed_at",
        "changed_by",
        "metadata",
    )

    readonly_fields_new_base = (
        # "id",
        "owner",
        # "created_at",
        # "changed_at",
        # "changed_by",
        # "metadata",
    )

    list_display_base = (
        # "id",
        "owner",
        "created_at",
        "changed_at",
        "changed_by",
        # "metadata",
    )

    search_fields_base = (
        "id",
        # "owner",
        # "created_at",
        # "changed_at",
        # "changed_by",
        # "metadata",
    )

    list_filter_base = (
        # "id",
        "owner",
        # "created_at",
        # "changed_at",
        "changed_by",
        # "metadata",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user

        super().save_model(request, obj, form, change)


class DefaultModelInlineMixin(object):
    # Default values that can be overwritten in each child class:
    fields = ()
    readonly_fields = ()

    # Default values that can be overwritten in each child mixin:
    fields_base = ()
    readonly_fields_base = ()

    extra = 0
    show_change_link = True

    def get_fields(self, request, obj=None):
        return self.fields + self.fields_base

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields_base + self.readonly_fields


class BaseModelInlineMixin(DefaultModelInlineMixin):
    fields_base = (
        # "id",
        "owner",
        "created_at",
        "changed_at",
        "changed_by",
        # "metadata",
    )

    readonly_fields_base = (
        # "id",
        "owner",
        "created_at",
        "changed_at",
        "changed_by",
        # "metadata",
    )


class ReadOnlyModelMixin(object):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
