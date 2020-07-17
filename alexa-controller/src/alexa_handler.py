# -*- coding: utf-8 -*-

import json
import logging
import boto3
import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.dispatch_components import (
AbstractRequestHandler, AbstractExceptionHandler,
AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.response_helper import (
get_plain_text_content, get_rich_text_content)

from ask_sdk_model.interfaces.display import (
ImageInstance, Image, RenderTemplateDirective, ListTemplate1,
BackButtonBehavior, ListItem, BodyTemplate2, BodyTemplate1)
from ask_sdk_model import ui, Response

from custom_modules import data, util, questions, score
    

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# iot = boto3.client('iot-data', region_name='us-east-1')


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        handler_input.response_builder.speak(data.WELCOME_MESSAGE).ask(data.HELP_MESSAGE)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        print("Session ended with reason: {}".format(handler_input.request_envelope))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        handler_input.attributes_manager.session_attributes = {}
        # Resetting session
        
        handler_input.response_builder.speak(data.HELP_MESSAGE).ask(data.HELP_MESSAGE)
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop and Pause intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.PauseIntent")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        handler_input.response_builder.speak(
                                             data.EXIT_SKILL_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response




class StartQuizIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("start_quiz_intent")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In StartQuizIntentHandler")
        attr = handler_input.attributes_manager.session_attributes
        language = handler_input.request_envelope.request.locale.split('-')[0]
        user_id = handler_input.request_envelope.session.user.user_id

        # GETS USER CURRENT SCORE
        user_score = score.get_score(user_id)
        print(user_score)

        # ASK CAPITAL OF RANDOM COUNTRY
        # TODO: CHOOSE COUNTRY BY DIFICULTY
        q = questions.get_question()
        attr['answer'] = q['answer']
        attr['country'] = q['country']
        
        rsp = random.choice(data.I18N[language]['QUIZ_QUESTION']).format(country=q['country'])
        
        response_builder = handler_input.response_builder
        response_builder.speak(rsp).ask(rsp)
        
        return response_builder.response



class AnswerIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return (is_intent_name("answer_intent")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In StartQuizIntentHandler")
        attr = handler_input.attributes_manager.session_attributes
        language = handler_input.request_envelope.request.locale.split('-')[0]
        user_id = handler_input.request_envelope.session.user.user_id

        # GETS USER ANSWER AND COMPARES TO CORRECT ANSWER
        slots = handler_input.request_envelope.request.intent.slots
        print(slots)

        #answer = slots["capital"].resolutions.resolutions_per_authority[0].values[0].value.id
        answer = slots["capital"].value
        print(answer)
        print(attr['answer'])

        is_correct = (answer.lower() == attr['answer'].lower())
        print(is_correct)

        # UPDATES THE QUESTION SCORE TO MEASURE QUESTION DIFFICULTY
        qr = questions.update_question_global_score(attr["country"], is_correct)
        print(qr)

        # UPDATES THE USER'S SCORE
        sr = score.update_user_score(user_id, is_correct)
        print(sr)
        

        if is_correct:
            rsp = random.choice(data.I18N[language]['CORRECT_ANSWER'])
            card_title = data.I18N[language]['CORRECT_TITLE']
        else: 
            rsp = random.choice(data.I18N[language]['WRONG_ANSWER']) + random.choice(data.I18N[language]['QUESTION_ANSWER']).format(capital=attr['answer'])
            card_title = data.I18N[language]['WRONG_TITLE']


        # card_img_url = util.get_card_icon("solvimm/solvimm-logo-white.png")
        #, image = ui.Image(small_image_url = card_img_url, large_image_url = card_img_url))
        
        q = questions.get_question()
        attr['answer'] = q['answer']
        attr['country'] = q['country']
        rsp += random.choice(data.I18N[language]['QUIZ_QUESTION']).format(country=q['country'])

        card = ui.StandardCard(title = card_title, text = rsp)
        
        response_builder = handler_input.response_builder
        response_builder.speak(rsp).ask(rsp).set_card(card)
        
        return response_builder.response


class RepeatHandler(AbstractRequestHandler):
    """Handler for repeating the response to the user."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        if "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(
                                                              cached_response_str, Response)
            return cached_response
        else:
            response_builder.speak(data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)
            
            return response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent.
        2018-May-01: AMAZON.FallackIntent is only currently available in
        en-US locale. This handler will not be triggered except in that
        locale, so it can be safely deployed for any locale."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        handler_input.response_builder.speak(
                                             data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)
                                             
        return handler_input.response_builder.response


# Interceptor classes
class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.
        The interceptor is used to cache the handler response that is
        being sent to the user. This can be used to repeat the response
        back to the user, in case a RepeatIntent is being used and the
        skill developer wants to repeat the same information back to
        the user.
        """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.
        This handler catches all kinds of exceptions and prints
        the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True
    
    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        
        speech = "Ops! Tivemos um problema. Você pode repetir?"
        handler_input.response_builder.speak(speech).ask(speech)
        
        attr = handler_input.attributes_manager.session_attributes
        attr["state"] = ""
        
        return handler_input.response_builder.response

# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
                                                  handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))



# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RepeatHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())


# Add all request handlers to the skill.
sb.add_request_handler(StartQuizIntentHandler())
sb.add_request_handler(AnswerIntentHandler())


# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add response interceptor to the skill.
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
