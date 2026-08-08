import json

fixes = {
 "e15": [
   ("Det hjälter att sänka andningstakten.", "Det hjälper att sänka andningstakten."),
   ("kanske till och med en panikattack", "kanske till och med en panikattack"),
 ],
 "e16": [
   ("mellangrändsområde", "mellangärdesområde"),
   ("tummmen", "tummen"),
   ("syntes lika tyglydligt som tystnaden", "syntes lika tydligt som tystnaden"),
 ],
 "e21": [
   ("När man mörker någon man inte tycker om", "När man möter någon man inte tycker om"),
   ("På formar festen", "På festen"),
 ],
 "e22": [
   ("hos spädbarat", "hos spädbarn"),
   ("känner sig elleromm trygg", "känner sig trygg"),
   ("mot denandra", "mot den andra"),
   ("spädöbarn", "spädbarn"),
   ("ju längre kvällen, desto mer visade", "ju längre kvällen led, desto mer visade"),
 ],
 "e23": [
   ("Vid dejting ser de att en person lutar sig framåt och den andra, om den känner sig trygg, härmar det.", "Vid dejting ser man att en person lutar sig framåt och att den andra, om den känner sig trygg, härmar beteendet."),
 ],
 "e24": [
   ("under efter att under do na", "under långa"),
   ("Det är en del avs frysresponsen", "Det är en del av frysresponsen"),
   ("supelisförhör", "polisförhör"),
   ("när di", "när man"),
   ("i tjugo minuten, axlarna spända och ryggra rak", "i tjugo minuter, axlarna spända och ryggen rak"),
 ],
 "e25": [
   ("säker b skydda sin hänsynsida", "skydda sin ventigm sida"),
   ("uppsett hot", "upplevt hot"),
   ("som om inga skulle märka det", "som om ingen skulle märka det"),
 ],
 "e26": [
   ("I formella sammanhang bör man och göra.", "I formella sammanhang bör man undvika det."),
   ("na hopsjunkna from vegan var lygiltig", "den hopsjunkna hållningen förmedlade likgiltigheten"),
   ("ett omd om att là khong", "ett budskap om att han inte rydde sig"),
   ("visa sina föräld inventor", "visa sina föräldrar"),
   ("ett budskap om att han inte rydde sig", "ett budskap om att han inte brydde sig"),
 ],
 "e27": [
   ("som om de had flavor", "som om de hade magmsmärtor"),
   ("Oftagör de det med armarna seller as manger", "Ofta gör de det med armarna lagda över magen"),
   ("böglade", "böde"),
   ("träffat honom yg i magen", "träffat honom i magen"),
 ],
 "e28": [
   ("övervigad av kän gods att", "övervigad av känslor"),
   ("Patients annars också hålryttena", "Hon kan också hålla en kudden"),
   ("ett eticenskivt gräl", "ett intensivt gräl"),
 ],
 "e29": [
   ("den ve hå svåra", "den svåra"),
 ],
 "e31": [
   ("inför sängskröten", "halsgropen"),
   ("för det att skda bron", "tydig för att skydda fosteret"),
   ("dom åsliga restaurangen", "den bullriga restaurangen"),
   ("höjare", "höger"),
 ],
 "e32": [
   ("och viss forskares anser att det til och med man", "och vissa forskare anser att det till och med hjälper"),
   ("på magen i cirklan", "på magen i cirklar"),
   ("upprepningen lugnande henne", "upprepningen lugnade henne"),
 ],
 "e33": [
   ("Människor kan ära det under", "Människor kan göra det under"),
   ("strax efteréå", "strax efteråt"),
   ("Det el skall syn sällan hos fyra relationen", "Det syn sällan hos par i början av en relation"),
   ("vikade", "vickade"),
   ("Klanumpan", "rumpan"),
 ],
 "e34": [
   ("höftens och benens blådor", "höftens och benens sidor"),
   ("hos resenistes som går igenom tullen", "hos resenärer som går igenom tullen"),
   ("gnuggade den nervös pendlan på sidorna av höfterna och verktyget fann benen med handfltorna", "gnuggade den nervöse resenären på sidoran av höfterna och benen med handflatorna"),
 ],
 "e35": [
   ("men gor det också känns behagligt", "men gör att det också känns behagligt"),
 ],
 "e36": [
   ("chockade många den vist utfö", "chockade många när det först utfördes"),
   ("grna van", "ganska vanbo"),
   ("varför enheim m½", "varför en del män"),
   ("theory", "teorier"),
   ("för att gäcka uppmärksamhet", "för att fä uppmärksamhet"),
   ("sitta ben", "sitta sak"),
   ("till exempel op en firma", "till exempel på ett kontor"),
   ("är hur vanlig", "är ganska vanlig"),
 ],
 "e13": [
  ("skjuter saker ifrån sig: den misstänkte som vägrar röra","skjuter saker ifrån sig: den misstänkte")
 ],
 "e15": [
   ("tyder på ett enhets och", "tyder på rädsla eller ångest"),
   ("inadning", "in andra"),
   ("yand in ut", "andas ut"),
   ("and a och in and", "andas ut och in"),
 ],

}
import json,glob,re,os
for num,smap in fixes.items():
    f=os.path.join(r'extract\tools',num+'.json')
    txt=open(f,encoding='utf-8').read()
    for old,new in smap:
        if old in txt:
            txt=txt.replace(old,new)
            print(num,'ok:',old[:40])
        else:
            print(num,'MISS:',old[:50])
    open(f,'w',encoding='utf-8').write(txt)