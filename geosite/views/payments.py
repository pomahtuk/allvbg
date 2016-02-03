import hashlib
from datetime import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from accounts.models import User
from geosite.models import OrdersList


def result(request):
    mrh_pass2 = ""
    out_sum = request.GET['OutSum']
    inv_id = request.GET['InvId']
    crc = request.GET['SignatureValue']

    temp = out_sum + ":" + inv_id + ":" + mrh_pass2
    my_crc = hashlib.md5(temp).hexdigest()

    if my_crc.upper() == crc.upper():
        msg = "OK" + inv_id + "\n"
    else:
        msg = "bad sign\n"
    return render_to_response("agenda/blank.html", {"msg": msg, }, )


def pay(request):
    # TODO: set payment rules from admin

    if request.method == 'POST':
        out_sum = request.POST['OutSum']
        if out_sum == "50":
            mth = "1"
        elif out_sum == "90":
            mth = "2"
        elif out_sum == "135":
            mth = "3"
        elif out_sum == "250":
            mth = "6"
        elif out_sum == "450":
            mth = "12"
        inv_desc = "Payment for editing firm by user with id = " + request.POST['desc'] + " for " + mth + " month(s)"
        mrh_login = ""
        mrh_pass1 = ""

        m = str(date.today().month)
        if len(m) == 1:
            m = "0" + m
        d = str(date.today().day)
        if len(d) == 1:
            d = "0" + d
        y = str(date.today().year)

        usr = User.objects.get(pk=request.POST['desc'])
        order = OrdersList(user=usr, summ=out_sum, date=datetime.now(), lng=inv_desc)
        order.save()

        inv_id = str(order.id)

        string = mrh_login + ":" + out_sum + ":" + inv_id + ":" + mrh_pass1

        crc = hashlib.md5(string).hexdigest()

        # uncomment after tests done
        url = "https://merchant.roboxchange.com/Index.aspx?MrchLogin=" + mrh_login + "&OutSum=" + out_sum + "&InvId=" + inv_id + "&Desc=" + inv_desc + "&SignatureValue=" + crc;

        return HttpResponseRedirect(url)


def pay_ok(request):
    # TODO: set payment rules from admin
    if request.method == 'GET':
        out_sum = request.GET['OutSum']
        inv_id = request.GET['InvId']
        crc = request.GET['SignatureValue']
        mth = 0
        mrh_pass1 = ""
        mrh_login = ""
        mrh_pass2 = ""

        temp = out_sum + ":" + inv_id + ":" + mrh_pass1
        my_crc = hashlib.md5(temp).hexdigest()

        if crc == my_crc:
            if out_sum == "50":
                mth = 1
            elif out_sum == "90":
                mth = 2
            elif out_sum == "135":
                mth = 3
            elif out_sum == "250":
                mth = 6
            elif out_sum == "450":
                mth = 12

            order = OrdersList.objects.get(pk=inv_id)

            y = 0
            if mth == 12:
                mth = 0
                y = 1

            dt = datetime(order.date.year + y, order.date.month + mth, order.date.day)
            up = order.user.get_profile()
            up.paid_till = dt
            up.save()
            return HttpResponseRedirect('/accounts/profile/')
        else:
            return render_to_response("site/bootstrap/base.html", context_instance=RequestContext(request))
    return HttpResponseRedirect('/accounts/profile/')

