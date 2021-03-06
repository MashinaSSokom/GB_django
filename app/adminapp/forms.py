from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from django.forms import ModelForm
from django import forms
from django import forms


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'
        exclude = ('date_joined', 'is_staff', 'groups', 'user_permissions', 'last_login',)

    def __init__(self, *args, **kwargs):
        super(ShopUserAdminEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.__class__ == forms.fields.BooleanField:
                field.widget.attrs['class'] = 'form-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''


class ProductCategoryFrom(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'is_active')

    def __init__(self, *args, **kwargs):
        super(ProductCategoryFrom, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.__class__ == forms.fields.BooleanField:
                field.widget.attrs['class'] = 'form-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''


class ProductFrom(ModelForm):
    class Meta:
        model = Product
        exclude = ('created', 'updated',)
        # widgets = {'category': forms.widgets.Select(attrs={'readonly': True,
        #                                                    'disabled': True})}

    def __init__(self, *args, **kwargs):
        super(ProductFrom, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.__class__ == forms.fields.BooleanField:
                field.widget.attrs['class'] = 'form-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''


class ProductEditForm(ShopUserEditForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('created', 'updated', 'category')

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.__class__ == forms.fields.BooleanField:
                field.widget.attrs['class'] = 'form-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''
