from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'
        exclude = ('date_joined', 'is_staff', 'groups', 'user_permissions', 'last_login',)
