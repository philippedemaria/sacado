from django import template
from django.apps import apps
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
def at_index(array, index):
    return array[index]

@register.filter
def to_int(value):
    return int(value)


@register.filter
def param_to_object(obj, student_id, period_id):
    return obj.score(student_id, period_id)


@register.filter
@stringfilter
def strip(value):
    return value.strip()



@register.simple_tag
def get_list_by_theme(obj, student_id, period_id):
    return obj.list_by_theme(student_id, period_id)


@register.simple_tag
def get_list_by_theme_student_period(theme_id,student_id, period_id):
    Theme = apps.get_model('socle', 'Theme')
    return Theme.list_by_student_period(theme_id,student_id, period_id)



@register.simple_tag
def get_list_by_knowledge(knowledge_id, student_id, period_id):
    return EvaluateKnowledge.list_by_knowledge(knowledge_id, student_id, period_id)



@register.simple_tag
def get_comment_from_livretsubject_by_theme_and_subject(livret_id, subject_id):
	LivretSUBJECT = apps.get_model('livret', 'livretSUBJECT')
	return LivretSUBJECT.comment_from_livretsubject_by_theme_and_subject(livret_id, subject_id)


@register.simple_tag
def get_list_by_subject_student_period(subject_id,student_id, period_id):
    Knowledge = apps.get_model('socle', 'Knowledge')
    return Knowledge.list_by_subject(subject_id,student_id, period_id)


@register.simple_tag
def get_list_by_subject(obj, subject_id, cycle_id):
    return obj.list_by_subject(subject_id, cycle_id)


@register.simple_tag
def get_score(obj, student_id, period_id):
    return obj.score(student_id, period_id)

@register.simple_tag
def get_score_by_theme(theme_id, student_id, period_id):
    Theme = apps.get_model('socle', 'Theme')
    return Theme.score_by_theme(theme_id, student_id, period_id)


@register.simple_tag
def get_score_by_subject(subject_id, student_id, period_id):
    Subject = apps.get_model('socle', 'Subject')
    return Subject.score_by_subject(subject_id, student_id, period_id)

@register.simple_tag
def get_score_from_livretsubject_by_theme_and_subject(livret_id, subject_id):
    LivretSUBJECT = apps.get_model('livret', 'livretSUBJECT')
    return LivretSUBJECT.score_from_livretsubject_by_theme_and_subject(livret_id, subject_id) 




@register.simple_tag
def get_nb_evaluated(obj, teacher_id):
    return obj.nb_evaluated(teacher_id)



@register.simple_tag
def get_livret_id_from_student_and_period_id(obj,period_id):
    return obj.livret_id_from_student_and_period_id(period_id)
 