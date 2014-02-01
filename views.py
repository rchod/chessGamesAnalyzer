from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from urllib import urlencode
import urllib2, sys
from bs4 import BeautifulSoup
from collections import Counter

def home(request2):
    return render(request2, 'index.html', {})

def analyze(request2):
    won_white=0
    won_black=0
    lost_black=0
    lost_white=0
    draw_white=0
    draw_black=0
    total=0
    timec=0
    timeline = list()
    timeline2 = list()
    win_f_moves = list()
    loss_f_moves = list()
    draw_f_moves = list()
    w_moves = list()
    b_moves = list()
    w_termination = list()
    l_termination = list()
    time_controls = list()
    member=request2.POST['member']
    for page in range(1,3):
      data = urlencode({'sortby': '', 'show': 'live', 'member': member, 'page': page })
      request = urllib2.Request('http://www.chess.com/home/game_archive?'+data)
      response = urllib2.urlopen(request, timeout=10)
      content = response.read()
      soup = BeautifulSoup(content)
      
      for i,item in enumerate(soup.find_all("a", class_="games")):
        game_id = item.get('href')[19:]
        #print "retreiving games ... game "+game_id
        request = urllib2.Request('http://www.chess.com/echess/download_pgn?lid='+game_id)
        content = urllib2.urlopen(request, timeout=10).read()
        parts=content.splitlines()
        date=parts[2][12:-2]
        white=parts[3][8:-2]
        black=parts[4][8:-2]
        result=parts[5][9:-2]
        white_elo=parts[6][11:-2]
        black_elo=parts[7][11:-2]
        timeControl=parts[8][14:-2]
        termination=parts[9][14:-2]
        first_move=parts[11].split()[0][2:]
        time_controls.append(timeControl)
        timec=float(timeControl.split("|")[0])
        try:
          second_move=parts[11].split()[1]
        except:
          pass
        term=termination.split()[-1]
        
        if white==member:
          if timec < 3:
            timeline.append([date,white_elo])
          if timec >= 3 and timec < 15:
            timeline2.append([date,white_elo])
        if black==member:
          if timec < 3:
            timeline.append([date,black_elo])
          if timec >= 3 and timec < 15:
            timeline2.append([date,black_elo])
        if white==member and result=="1-0":
          won_white=won_white+1
          w_moves.append(first_move)
          w_termination.append(term)
        if black==member and result=="1-0":
          won_black=won_black+1
          b_moves.append(second_move)
          w_termination.append(term)
        if white==member and result=="0-1":
          lost_white=lost_white+1
          l_termination.append(term)
          w_moves.append(first_move)
        if black==member and result=="0-1":
          lost_black=lost_black+1
          b_moves.append(second_move)
          l_termination.append(term)
        if black==member and result=="1/2-1/2":
          draw_black=draw_black+1
          b_moves.append(second_move)
        if white==member and result=="1/2-1/2":
          w_moves.append(first_move)
          draw_white=draw_white+1
        total=total+1
    return render(request2, 'analyze.html', {'total': total,'won_white': won_white,'won_black': won_black,'lost_black': lost_black,'lost_white': lost_white,'draw_white': draw_white,'draw_black': draw_black,'won':won_white+won_black,'lost':lost_white+lost_black,'draw':draw_white+draw_black,'w_moves':Counter(w_moves).items(),'b_moves':Counter(b_moves).items(),'l_termination':Counter(l_termination).items(),'w_termination':Counter(w_termination).items(),'timeline':timeline,'timeline2':timeline2,'time_controls':Counter(time_controls).items()})


