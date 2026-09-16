from django.contrib import admin
from .models import Author, Book, BookDetail, Genre, Loan,  Review
# Register your models here.
from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

admin.site.site_header = "Administrador de MiniLibrary"
admin.site.site_title = "Panel"
admin.site.index_title = "Realiza las modificaciones desde este panel!"


@admin.action(description="Marcar prestamos como devueltos")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned=True)


@admin.action(description="Marcar devueltos como prestados")
def mark_as_loan(modeladmin, request, queryset):
    queryset.update(is_returned=False)


class LoanInline(admin.TabularInline):
    model = Loan
    extra = 1

    # UNO A MUCHOS


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False
    verbose_name_pural = "Detalle del libro"


class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]
    list_display = ("username", "email")

# registrar mediante decoradores


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, BookDetailInline]
    list_display = ("title", "author", "pages", "publication_date")
    search_fields = ("title", "author__name")
    list_filter = ("author", "genres", "publication_date")
    ordering = ["-publication_date"]
    date_hierarchy = "publication_date"
    auto_complete_fields = ["author", "genres"]
    fieldsets = (("informacion general", {
        "fields": ("title", "author", "publication_date", "genres")
    }), (
        "Detalles", {
            "fields": ("isbn", "pages"),
            "classes": ("collapse",)
        }
    ))
    # ASIGNANDO PERMISOS DESDE CODIGO

    def has_add_permission(self, request):
        # return super().has_add_permission(request)
        return request.user.is_superuser

    def has_change_permission(self, request, obj=...):
        return request.user.is_staff


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ("loan_date",)
    list_display = ("user", "book", "loan_date", "is_returned")
    actions = [mark_as_returned, mark_as_loan]
    raw_id_fields = ["user", "book"]


# admin.site.register(Author,AuthorAdmin)
# admin.site.register(Book, admin_class=BookAdmin)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
# admin.site.register(Genre,GenreAdmin)
admin.site.register(Review)
# admin.site.register(Loan,LoanAdmin)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
