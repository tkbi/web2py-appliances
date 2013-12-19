NE = IS_NOT_EMPTY()
def Required(*a,**b): return b.update({'requires':NE}) or Field(*a,**b)
def Readonly(*a,**b): return b.update({'writable':False}) or Field(*a,**b)
def Hidden(*a,**b): return b.update({'readable':False}) or Readonly(*a,**b)
def Unique(*a,**b): return b.update({'unique':True}) or Field(*a,**b)
def Reference(name,**b): return Hidden(name,'reference '+name,**b)
def ListStrings(name, set): return Field(name,'list:string',requires=IS_IN_SET(set,multiple=True))
tags = Field('tags','list:string',compute=lambda row: row.name.split())

db.define_table(
    'forum',
    Required('name'),
    Field('body','text'),
    Hidden('html','text',compute=lambda row: MARKMIN(row.body or '').xml()),
    Readonly('views','integer',default=0),
    Readonly('last_updated','datetime',default=request.now),
    auth.signature)

db.define_table(
    'post',
    Reference('forum'),
    Field('parent_id','reference post'),
    Required('body','text'),
    Hidden('html','text',compute=lambda row: MARKMIN(row.body or '').xml()),
    Hidden('reported','boolean'),
    Hidden('approved','boolean'),
    Hidden('banned','boolean'),
    Hidden('deleted','boolean'),
    auth.signature)


def make_up():
    images = ['http://matplotlib.org/_images/errorbar_demo_features.png',
              'http://matplotlib.org/_images/scatter_demo1.png',
              'http://matplotlib.org/_images/streamplot_demo_masking.png',
#              'http://matplotlib.org/_images/spines_demo_bounds.png',
#              'http://matplotlib.org/_images/scatter_hist1.png',
              'http://freedownloads.last.fm/download/414521506/Heartbeat.mp3',
              'http://www.auby.no/files/video_tests/h264_720p_hp_5.1_6mbps_ac3_planet.mp4']

    formulas = [r'\( \sum_i \frac{i(i+1)}{2} \)',
                r'\( \int _a ^b \sin(x) \cos^3(x) dx \)',
                r'\( B^{ast} \rightarrow B^0 + \pi^{+} \)',
                r'\( \pi^0 \rightarrow \gamma + \gamma \)']
    import random
    from gluon.contrib.populate import populate, IUP, Learner
    db(db.forum).delete()
    db(db.post).delete()
    populate(db.forum,20)
    ell = Learner()
    ell.loadd(IUP)
    for forum in db(db.forum).select():
        db.post.forum.default=forum.id
        id = None
        for k in range(random.randint(10,30)):
            n = random.choice((20,25,50,100,200))
            body = body=ell.generate(n, prefix=None)
            if random.random()<0.3:
                body += '\n'+random.choice(images)
            elif random.random() <0.3:
                body += '\n'+random.choice(formulas)
            id = db.post.insert(forum=forum.id,parent_id=id, body=body)
            if random.choice((0,1)): id = None
        db.commit()

if DEBUG and db(db.forum).isempty(): make_up()
