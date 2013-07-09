from modeltranslation.translator import translator, TranslationOptions
from allvbg.models import *

class FirmTranslationOptions(TranslationOptions):
    fields = ('short', 'description', 'name',)

class EventTranslationOptions(TranslationOptions):
    fields = ('short', 'description', 'name',)
	
translator.register(Firm, FirmTranslationOptions)
translator.register(Event, EventTranslationOptions)