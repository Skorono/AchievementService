from flasgger import Swagger
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_injector import FlaskInjector
from flask_marshmallow import Marshmallow
from flask_restful import Api

from api.config import InjectorConfig
from api.resources.user_resource import UserAPI, UsersAPI, UserAchievementsAPI, UserStatisticScoreLeaderAPI
from core.services.user_service import UserService

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'AchievementService API',
    'uiversion': 3
}

swagger = Swagger(app)

docs = FlaskApiSpec(app)

ma = Marshmallow(app)

injector: FlaskInjector = FlaskInjector(app=app, modules=[InjectorConfig.configure])

api.add_resource(UserAPI, '/user', '/user/<int:user_id>',
                 resource_class_kwargs={'service': injector.injector.get(UserService)})

api.add_resource(UsersAPI, '/users',
                 resource_class_kwargs={'service': injector.injector.get(UserService)})

api.add_resource(UserAchievementsAPI, '/user/<int:user_id>/achievements',
                 resource_class_kwargs={'service': injector.injector.get(UserService)})

api.add_resource(UserStatisticScoreLeaderAPI, '/user/statistic/score_leader',
                 resource_class_kwargs={'service': injector.injector.get(UserService)})

if __name__ == "__main__":
    app.run(port=8080, debug=True)
