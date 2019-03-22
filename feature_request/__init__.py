from . import factories

app = factories.create_app('feature_request', 'config.Config')

from feature_request.views import public

factories.initialize_blueprints(app, public.www)

