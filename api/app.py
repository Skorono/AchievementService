import logging

from flasgger import Swagger
from flask import Flask, Blueprint
from flask_apispec import FlaskApiSpec
from flask_injector import FlaskInjector
from flask_marshmallow import Marshmallow
from flask_restful import Api

from api.config import InjectorConfig
from api.resources.achievement_resource import AchievementAPI, AchievementsAPI
from api.resources.user_resource import UserAPI, UsersAPI, UserAchievementsAPI, UserStatisticScoreLeaderAPI, \
    UserStatisticAchievementLeaderAPI, UserStatisticMinDiffUsersAPI
from core.services.achievement_service import AchievementService
from core.services.user_service import UserService, UserStatisticService, IUserAchievementsService, \
    UserAchievementsService

app = Flask(__name__)

app.config["SWAGGER"] = {
    "openapi": "3.0.2",
    "uiversion": 3
}

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

#Все что автоматически генерит документацию сдалось под гнетом injector`а
#https://github.com/python-injector/flask_injector/issues/78
swagger = Swagger(app, template_file='./api-specs/api-specs.yml')

docs = FlaskApiSpec(app)

ma = Marshmallow(app)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

injector: FlaskInjector = FlaskInjector(app=app, modules=[InjectorConfig.configure])

api.add_resource(UserAPI, '/user',
                 resource_class_kwargs={'service': injector.injector.get(UserService)})

api.add_resource(UsersAPI, '/users',
                 resource_class_kwargs={'service': injector.injector.get(UserService)})

api.add_resource(UserAchievementsAPI, '/user/achievements',
                 resource_class_kwargs={'service': injector.injector.get(UserAchievementsService)})

api.add_resource(UserStatisticScoreLeaderAPI, '/user/statistic/score_leader',
                 resource_class_kwargs={'service': injector.injector.get(UserStatisticService)})

api.add_resource(UserStatisticAchievementLeaderAPI, '/user/statistic/achievement_leader',
                 resource_class_kwargs={'service': injector.injector.get(UserStatisticService)})

api.add_resource(UserStatisticMinDiffUsersAPI, '/user/statistic/min_score_diff',
                 resource_class_kwargs={'service': injector.injector.get(UserStatisticService)})

api.add_resource(AchievementAPI, '/achievement',
                 resource_class_kwargs={'service': injector.injector.get(AchievementService)})

api.add_resource(AchievementsAPI, '/achievements',
                 resource_class_kwargs={'service': injector.injector.get(AchievementService)})

app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run()
