from basthon2.models import ExoPython
from account.models import Teacher

g=ExoPython.objects.get(title="essai4")
g.instruction="""definir la fonction f qui rend la factorielle
du nombre entier naturel n passé en paramètre ; puis afficher f(10)"""
g.preambule_cache="""toto=17"""
g.preambule_visible="""########### fonction factorielle ##########"""
g.prog_cor="""def f(n):
    if n==0 : return 1
    return n*f(n-1)
print(f(10))
"""
g.teacher=Teacher.objects.get(user_id=1)
g.autotest="""print(f(0),f(1),f(2),f(20))"""
g.save()
