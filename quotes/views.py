from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
# Create your views here.
# quotes\views.py
from django.http import HttpResponseRedirect
from django.urls import reverse


days_of_week = {
    "monday": "el peor dia de la semana 🥲",
    "tuesday": "aun no carburo 🤕",
    "wednesday": "masomenos bien 😅",
    "thursday": "Ya casi es viernes 🙂",
    "friday": "Hoy es viernes chingo, gastar gastar dinero 🥳",
    "saturday": "aun es relajable el dia 😊",
    "sunday": "falio ferga raza es domingo 🤕"
}
day_number = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday"
}


def index(request):
    return render(request, 'quotes/index.html', {
        "days_of_week": days_of_week
    })


def weekNumber(request, day):
    try:
        # day_selected = day_number[day]
        days = list(days_of_week.keys())
        if day > len(days):
            return HttpResponseNotFound("No encontre tu pendejada maricon")
        # return HttpResponseRedirect(f"/quotes/{days[day - 1]}")
        day_name = days[day - 1]
        return HttpResponseRedirect(reverse('day-quote', args=[day_name]))
    except:
        return HttpResponseNotFound("No encontre tu pendejada padrino")


def weekdays(request, day):
    try:
        quotes_text = days_of_week[day]
        return HttpResponse(quotes_text)
    except KeyError:
        # return HttpResponse("no encontre tu pendejada, pon bien los dias de la semana en ingles padrino que no te los sabes maricon 😒")
        # return render(request, "404.html", status=404)
        raise Http404()

    except Exception:
        return HttpResponse("ni idea del error padrino")
