from django import template
 


register = template.Library()


######################################################################################
#### CES templates tags devraient aller dans Slackbot !!! en lien avec
####################################################################################

@register.simple_tag
def is_in_group(value,contact): 
    tab = []
    try : 
        for u in  contact.users.all() : 
            tab.append(u.id)
        test = False
        if value in tab :
            test = True
    except :
        test = False
    return test 

 