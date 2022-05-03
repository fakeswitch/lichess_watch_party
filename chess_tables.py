import json

legal_first_moves = {
'a3':'a2a3',
'a4':'a2a4',
'b3':'b2b3',
'b4':'b2b4',
'c3':'c2c3',
'c4':'c2c4',
'd3':'d2d3',
'd4':'d2d4',
'e3':'e2e3',
'e4':'e2e4',
'f3':'f2f3',
'f4':'f2f4',
'g3':'g2g3',
'g4':'g2g4',
'h3':'h2h3',
'h4':'h2h4',
'na3':'b1a3',
'nc3':'b1c3',
'nf3':'g1f3',
'nh3':'g1h3',
}

eight_ball = [
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt',
    'Yes definitely.',
    'You may rely on it.',
    'As I see it, yes.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Signs point to yes.',
    'Reply hazy, try again.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don\'t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.'
]

animal_subreddits = [
    'aww',
    'cats',
    'goldenretrievers',
    'rarepuppers',
    'IllegallySmolCats',
    'Catswithjobs',
    'AnimalsBeingDerps',
    'dogswithjobs',
    'Eyebleach',
    'PuppySmiles',
    'catssittingdown',
    'politecats',
    'lookatmydog',
    'cromch',
    'CatsOnPizza',
    'dogswithsocks',
    'bearpuppers',
    'SupermodelCats',
    'OneOrangeBraincell',
    'hamsters',
    'catloaf'
]

#----------- horoscope!
with open(r'/home/ubuntu/git/lichess_stalker_bot/horo.json') as f:
   scope_dict = json.load(f)
