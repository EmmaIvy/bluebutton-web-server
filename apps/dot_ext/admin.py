from django import forms
from django.contrib import admin
from oauth2_provider.models import AccessToken
from oauth2_provider.models import get_application_model
from .forms import CustomRegisterApplicationForm
from .models import ApplicationLabel, AuthFlowUuid


Application = get_application_model()


class MyAccessToken(AccessToken):
    class Meta:
        proxy = True
        app_label = "bluebutton"


class MyApplication(Application):
    class Meta:
        proxy = True
        app_label = "bluebutton"


class MyAuthFlowUuid(AuthFlowUuid):
    class Meta:
        proxy = True
        app_label = "bluebutton"


class CustomAdminApplicationForm(CustomRegisterApplicationForm):
    description = forms.CharField(label="Application Description",
                                  help_text="Note text size and HTML tags are not validated under ADMIN.",
                                  widget=forms.Textarea, empty_value='', required=False)

    def __init__(self, *args, **kwargs):
        user = None
        super().__init__(user, *args, **kwargs)
        self.fields['logo_uri'].widget.attrs['readonly'] = False

    class Meta:
        model = MyApplication
        fields = (
            'client_id',
            'user',
            'client_type',
            'authorization_grant_type',
            'client_secret',
            'name',
            'skip_authorization',
            'scope',
            'require_demographic_scopes',
            'agree',
            'op_tos_uri',
            'op_policy_uri',
            'client_uri',
            'website_uri',
            'redirect_uris',
            'logo_uri',
            'logo_image',
            'tos_uri',
            'policy_uri',
            'software_id',
            'contacts',
            'support_email',
            'support_phone_number',
            'description',
            'active',
            'first_active',
            'last_active',
        )

    def clean(self):
        return self.cleaned_data

    def clean_agree(self):
        return self.cleaned_data.get('agree')


@admin.register(MyApplication)
class MyApplicationAdmin(admin.ModelAdmin):
    form = CustomAdminApplicationForm
    list_display = ("name", "user", "authorization_grant_type", "client_id",
                    "require_demographic_scopes", "scopes",
                    "created", "updated", "active", "skip_authorization")
    list_filter = ("client_type", "authorization_grant_type",
                   "require_demographic_scopes", "active", "skip_authorization")
    radio_fields = {
        "client_type": admin.HORIZONTAL,
        "authorization_grant_type": admin.VERTICAL,
    }

    search_fields = ('name', 'user__username', '=client_id', '=require_demographic_scopes', '=authorization_grant_type')

    raw_id_fields = ("user", )


@admin.register(MyAccessToken)
class MyAccessTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'application', 'expires', 'scope', 'token',)
    search_fields = ('user__username', 'application__name', 'token', 'source_refresh_token__token')
    raw_id_fields = ("user", 'application')


@admin.register(MyAuthFlowUuid)
class MyAuthFlowUuidAdmin(admin.ModelAdmin):
    list_display = ('created', 'auth_uuid', 'state', 'code', 'client_id',
                    'auth_pkce_method', 'auth_crosswalk_action', 'auth_share_demographic_scopes')
    search_fields = ('auth_uuid', 'state', 'code')


@admin.register(ApplicationLabel)
class ApplicationLabelAdmin(admin.ModelAdmin):
    model = ApplicationLabel
    filter_horizontal = ('applications',)
    list_display = ("name", "slug", "short_description")
    list_filter = ("name", "slug")
