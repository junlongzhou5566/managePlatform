from utils import passport
from web.views import index
from django.conf.urls import url
from web.views.ecs import ecs_index
from web.views.cdn import cdn_index
from web.views.user import vpn_index
from web.views.user import user_index
from web.views.server import server_index


urlpatterns = [
    url(r'^$', index.IndexView.as_view()),
    url(r'^logo.html$', index.LogoView.as_view()),

    url(r'^private$', index.PrivateView.as_view()),

    url(r'^login$', index.LoginView.as_view()),
    url(r'^logout$', index.LogoutView.as_view()),
    url(r'^login.html$', index.LoginView.as_view()),

    url(r'^public$', index.PublicView.as_view()),
    url(r'^public.html$', index.PublicSlbView.as_view()),

    url(r'^l$', index.MemberListView.as_view()),
    url(r'^welcome.html$', index.WelcomeView.as_view()),
    url(r'^host_info$', index.HostView.as_view()),

    url(r'^ecs_up_down$', index.EcsUpDownView.as_view()),
    url(r'^pub_slb_ecs_up_down$', index.PublicSlbEcsUpDownView.as_view()),

    url(r'^passport$', passport.PassportAPI.as_view()),

    url(r'^cdn$', cdn_index.CDNIndexView.as_view()),
    url(r'^cdn.html$', cdn_index.CDNRefreshView.as_view()),

    url(r'^user$', user_index.UserIndexView.as_view()),
    url(r'^user.html$', user_index.UserListView.as_view()),
    url(r'^user_edit-(\w+).html$', user_index.UserEditView.as_view()),
    url(r'^userEdit$', user_index.UserEditPostView.as_view()),
    url(r'^user_add.html$', user_index.UserAddView.as_view()),

    url(r'^user_forbidden$', user_index.UserForbiddenView.as_view()),
    url(r'^user_start$', user_index.UserStartView.as_view()),
    url(r'^reset_pwd$', user_index.ResetPwdView.as_view()),

    url(r'^ecs$', ecs_index.EcsIndexView.as_view()),
    url(r'^ecs.html$', ecs_index.EcsListView.as_view()),
    url(r'^create_ecs.html$', ecs_index.CreateEcsView.as_view()),

    url(r'^server$', server_index.ServerIndexView.as_view()),
    url(r'^server.html$', server_index.ServerListView.as_view()),

    url(r'^test$', index.TestView.as_view()),
    url(r'^fs-test.html$', index.FsTestView.as_view()),

    url(r'^forbidden_vpn$', vpn_index.ForbiddenVpn.as_view()),
    url(r'^start_vpn$', vpn_index.StartVpn.as_view()),
]
