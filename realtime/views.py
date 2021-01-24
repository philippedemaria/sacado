from django.shortcuts import render

# Create your views here.

def as_ck(request):
	context =  {}
	return render(request,'realtime/as_ck.html',context)
