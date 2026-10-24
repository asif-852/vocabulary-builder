import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

# Master curation dictionary for GRE 333 Sets 1 to 10 (Words 1 to 200)
# Format: index -> (pos, pron_en, pron_bn, meaning_en, clean_meaning_bn, syns, ants)
CURATED_DATA = {
    1: ('verb', 'uh-BAYT', 'আ-বেইট', 'To lessen, diminish, or reduce in intensity or amount.', 'কমানো বা তীব্রতা হ্রাস পাওয়া', ['subside', 'lessen', 'diminish'], ['intensify', 'increase', 'augment']),
    2: ('adjective', 'uh-BER-unt', 'আ-বের-অ্যান্ট', 'Departing from an accepted standard or normal type; atypical.', 'বিপথগামী বা অস্বাভাবিক', ['abnormal', 'deviant', 'atypical'], ['normal', 'typical', 'regular']),
    3: ('noun', 'uh-BAY-unss', 'আ-বেই-অ্যান্স', 'A state of temporary disuse, suspension, or dormancy.', 'সাময়িক স্থগিতাবস্থা', ['suspension', 'dormancy', 'latency'], ['continuation', 'resumption', 'activity']),
    4: ('verb', 'ab-SKOND', 'অ্যাব-স্কন্ড', 'To depart secretly and hurriedly, especially to avoid capture.', 'আত্মগোপন করা বা পালিয়ে যাওয়া', ['flee', 'escape', 'bolt'], ['remain', 'stay', 'appear']),
    5: ('adjective', 'ab-STEE-mee-us', 'অ্যাব-স্টি-মি-আস', 'Sparing or moderate in eating and drinking; temperate.', 'পানাহারে মিতব্যয়ী বা সংযমী', ['temperate', 'moderate', 'austere'], ['gluttonous', 'greedy', 'indulgent']),
    6: ('verb', 'ad-MON-ish', 'অ্যাড-মনিশ', 'To warn, caution, or scold gently but seriously.', 'সতর্ক করা বা মৃদু তিরস্কার করা', ['warn', 'reprove', 'scold'], ['praise', 'applaud', 'commend']),
    7: ('verb', 'uh-DUL-tuh-rayt', 'আ-ডাল-টা-রেইট', 'To make impure by adding inferior substances; contaminate.', 'ভেজাল মেশানো বা অপবিত্র করা', ['contaminate', 'taint', 'debase'], ['purify', 'refine', 'cleanse']),
    8: ('adjective', 'es-THET-ik', 'এস-থেট-ইক', 'Concerned with beauty or the appreciation of artistic taste.', 'নান্দনিক বা সৌন্দর্যবোধসম্পন্ন', ['artistic', 'tasteful', 'appealing'], ['unattractive', 'hideous', 'ugly']),
    9: ('verb', 'AG-ruh-gayt', 'অ্যাগ-রি-গেইট', 'To gather or combine into a single mass, total, or whole.', 'একত্রিত করা বা সমষ্টিগত করা', ['combine', 'accumulate', 'collect'], ['separate', 'disperse', 'scatter']),
    10: ('noun', 'uh-LAK-rih-tee', 'আ-ল্যাক-রি-টি', 'Brisk and cheerful readiness; prompt eagerness.', 'তৎপরতা বা সানন্দ আগ্রহ', ['eagerness', 'willingness', 'promptness'], ['reluctance', 'sluggishness', 'hesitation']),
    11: ('verb', 'uh-LEE-vee-ayt', 'আ-লি-ভি-এইট', 'To relieve, lessen, or make less severe.', 'উপশম বা লাঘব করা', ['relieve', 'ease', 'lessen'], ['worsen', 'aggravate', 'intensify']),
    12: ('verb', 'uh-MAL-guh-mayt', 'আ-মাল-গা-মেইট', 'To combine, merge, or unite into a unified whole.', 'একত্রিত বা মিশ্রিত করা', ['combine', 'merge', 'unite'], ['separate', 'divide', 'split']),
    13: ('adjective', 'am-BIG-yoo-us', 'অ্যাম-বিগ-ইউ-আস', 'Open to more than one interpretation; unclear or equivocal.', 'দ্ব্যর্থবোধক বা অস্পষ্ট', ['unclear', 'equivocal', 'vague'], ['clear', 'lucid', 'explicit']),
    14: ('noun', 'am-BIV-uh-lunss', 'অ্যাম-বিভ-আ-ল্যান্স', 'The state of having mixed, contradictory, or conflicting feelings.', 'দ্বিমুখী অনুভূতি বা দ্বিধাদ্বন্দ্ব', ['uncertainty', 'hesitation', 'indecision'], ['certainty', 'decisiveness', 'conviction']),
    15: ('verb', 'uh-MEEL-yuh-rayt', 'আ-মিল-ইও-রেইট', 'To make something better or more bearable; improve.', 'উন্নতিসাধন করা বা অবস্থার উন্নতি করা', ['improve', 'enhance', 'better'], ['worsen', 'deteriorate', 'damage']),
    16: ('noun', 'uh-NAK-ruh-niz-um', 'আ-নাক-র-নিজ-ম', 'Something placed out of its proper historical time period.', 'কালবৈষম্য বা যুগ-অনুপযোগী বস্তু', ['misplacement', 'archaism', 'incongruity'], ['modernity', 'synchronism', 'currency']),
    17: ('adjective', 'uh-NAL-uh-gus', 'আ-ন্যা-লা-গাস', 'Comparable in certain respects; similar in function.', 'সদৃশ বা তুলনীয়', ['comparable', 'similar', 'parallel'], ['different', 'dissimilar', 'unrelated']),
    18: ('noun', 'AN-er-kee', 'অ্যান-আর-কি', 'A state of disorder due to absence of authority or government.', 'নৈরাজ্য বা বিশৃঙ্খলা', ['chaos', 'disorder', 'lawlessness'], ['order', 'rule', 'governance']),
    19: ('adjective', 'uh-NOM-uh-lus', 'আ-নম-আ-লাস', 'Deviating from what is standard, normal, or expected; irregular.', 'ব্যতিক্রমী বা অস্বাভাবিক', ['irregular', 'atypical', 'abnormal'], ['normal', 'standard', 'regular']),
    20: ('noun', 'an-TIP-uh-thee', 'অ্যান-টিপ-আ-থি', 'A deep-seated feeling of dislike, hostility, or aversion.', 'তীব্র বিদ্বেষ বা অনীহা', ['hostility', 'aversion', 'enmity'], ['sympathy', 'affection', 'affinity']),
    
    # Set 2 (21-40)
    21: ('noun', 'AP-uh-thee', 'অ্যাপ-আ-থি', 'Lack of interest, enthusiasm, or concern; indifference.', 'উদাসীনতা বা অনাগ্রহ', ['indifference', 'unconcern', 'passivity'], ['enthusiasm', 'passion', 'concern']),
    22: ('verb', 'uh-PEEZ', 'আ-পীজ', 'To pacify or placate someone by acceding to their demands.', 'শান্ত বা তুষ্ট করা', ['pacify', 'placate', 'soothe'], ['provoke', 'irritate', 'enrage']),
    23: ('verb', 'uh-PRYZ', 'আ-প্রাইজ', 'To inform, notify, or tell someone of something.', 'অবহিত করা বা জানানো', ['inform', 'notify', 'advise'], ['mislead', 'conceal', 'hide']),
    24: ('noun', 'ap-ruh-BAY-shun', 'অ্যাপ-রা-বেই-শান', 'Approval, praise, or official commendation.', 'অনুমোদন বা প্রশংসা', ['praise', 'approval', 'commendation'], ['disapproval', 'criticism', 'censure']),
    25: ('verb', 'uh-PROH-pree-ayt', 'আ-প্রো-প্রি-এইট', 'To take possession of something for one’s own use, typically without permission.', 'অন্যায়ভাবে দখল করা বা আত্মসাৎ করা', ['seize', 'commandeer', 'usurp'], ['return', 'relinquish', 'surrender']),
    26: ('adjective', 'AHR-joo-us', 'আর-জু-আস', 'Involving or requiring strenuous effort; difficult and tiring.', 'কঠোর বা শ্রমসাধ্য', ['difficult', 'laborious', 'strenuous'], ['easy', 'effortless', 'simple']),
    27: ('adjective', 'AHRT-lis', 'আর্ট-লেস', 'Without guile, deceit, or craftiness; natural and sincere.', 'কপটতাহীন বা সরল', ['naive', 'candid', 'guileless'], ['cunning', 'crafty', 'deceitful']),
    28: ('adjective', 'uh-SET-ik', 'আ-সেট-ইক', 'Practicing strict self-denial and austerity, especially for spiritual reasons.', 'কঠোর তপস্বী বা আত্মসংযমী', ['austere', 'abstinent', 'monastic'], ['indulgent', 'hedonistic', 'luxurious']),
    29: ('adjective', 'uh-SIJ-oo-us', 'আ-সিজ-উ-আস', 'Showing great care, attention, and persistent effort; diligent.', 'অধ্যবসায়ী বা পরিশ্রমী', ['diligent', 'meticulous', 'persevering'], ['lazy', 'negligent', 'careless']),
    30: ('verb', 'uh-SWAYJ', 'আ-সোয়েজ', 'To make an unpleasant feeling less intense; soothe or relieve.', 'উপশম করা বা প্রশমিত করা', ['soothe', 'relieve', 'alleviate'], ['aggravate', 'intensify', 'worsen']),
    31: ('verb', 'uh-TEN-yoo-ayt', 'আ-টেন-ইউ-এইট', 'To reduce the force, thickness, or value of; weaken.', 'দুর্বল বা ক্ষীণ করা', ['weaken', 'reduce', 'diminish'], ['strengthen', 'amplify', 'intensify']),
    32: ('adjective', 'aw-DAY-shus', 'অ-ডেই-শাস', 'Showing a willingness to take surprisingly bold risks; fearless.', 'দুঃসাহসী বা নির্ভীক', ['bold', 'daring', 'fearless'], ['timid', 'cowardly', 'fearful']),
    33: ('adjective', 'aw-STEER', 'অ-স্টির', 'Severe or strict in manner; extremely plain and unadorned.', 'কঠোর বা সাদামাটা', ['strict', 'harsh', 'unadorned'], ['luxurious', 'lenient', 'ornate']),
    34: ('adjective', 'aw-TON-uh-mus', 'অ-টন-আ-মাস', 'Acting independently or having the freedom to do so; self-governing.', 'স্বায়ত্তশাসিত বা স্বাধীন', ['independent', 'self-governing', 'free'], ['dependent', 'subordinate', 'controlled']),
    35: ('verb', 'uh-VUR', 'আ-ভার', 'To state, assert, or declare with confidence.', 'দৃঢ়তার সাথে বলা বা ঘোষণা করা', ['assert', 'declare', 'affirm'], ['deny', 'refute', 'contradict']),
    36: ('adjective', 'buh-NAL', 'বা-নাল', 'So lacking in originality as to be obvious and boring; trite.', 'মামুলি বা গতানুগতিক', ['trite', 'clichéd', 'hackneyed'], ['original', 'fresh', 'novel']),
    37: ('verb', 'bih-LY', 'বি-লাই', 'To give a false impression of; contradict or disguise.', 'মিথ্যা প্রতিপন্ন করা বা বিপরীত ভাব প্রকাশ করা', ['contradict', 'misrepresent', 'disguise'], ['reveal', 'confirm', 'substantiate']),
    38: ('adjective', 'buh-NEF-ih-sunt', 'বা-নেফ-ই-স্যান্ট', 'Generous or doing good; actively charitable.', 'পরোপকারী বা কল্যাণকর', ['charitable', 'generous', 'altruistic'], ['malevolent', 'harmful', 'unkind']),
    39: ('verb', 'BOHL-ster', 'বোল-স্টার', 'To support, prop up, or strengthen.', 'দৃঢ় বা শক্তিশালী করা', ['support', 'strengthen', 'reinforce'], ['weaken', 'undermine', 'diminish']),
    40: ('adjective', 'bom-BAS-tik', 'বম-ব্যাস্ট-ইক', 'High-sounding but with little meaning; pompous or inflated.', 'বাগাড়ম্বরপূর্ণ বা দাম্ভিক', ['pompous', 'grandiloquent', 'pretentious'], ['humble', 'understated', 'simple']),

    # Set 3 (41-60)
    41: ('adjective', 'BOOR-ish', 'বুর-ইশ', 'Rough, unrefined, or ill-mannered in behavior; coarse.', 'অভদ্র বা চাষাড়ে স্বভাবের', ['crude', 'uncouth', 'churlish'], ['refined', 'polite', 'courteous']),
    42: ('verb', 'BUR-jun', 'বার-জান', 'To begin to grow or increase rapidly; flourish.', 'দ্রুত বৃদ্ধি পাওয়া বা বিকশিত হওয়া', ['flourish', 'thrive', 'expand'], ['wither', 'shrink', 'decline']),
    43: ('verb', 'BUR-nish', 'বার-নিশ', 'To polish something, especially metal, by rubbing.', 'ঘষে চকচকে বা উজ্জ্বল করা', ['polish', 'shine', 'buff'], ['tarnish', 'dull', 'damage']),
    44: ('verb', 'BUH-tris', 'বাট-রিস', 'To support, reinforce, or strengthen.', 'সমর্থন জোগানো বা শক্তিশালী করা', ['support', 'reinforce', 'bolster'], ['weaken', 'undermine', 'destroy']),
    45: ('adjective', 'kuh-PRISH-us', 'কা-প্রিশ-আস', 'Given to sudden, unaccountable changes of mood; fickle.', 'খামখেয়ালী বা পরিবর্তনশীল', ['fickle', 'unpredictable', 'whimsical'], ['steady', 'consistent', 'constant']),
    46: ('noun', 'kas-tih-GAY-shun', 'ক্যাস-টি-গেই-শান', 'Severe criticism or punishment; harsh rebuke.', 'কঠোর তিরস্কার বা ভর্ৎসনা', ['rebuke', 'chastisement', 'reprimand'], ['praise', 'commendation', 'applause']),
    47: ('noun', 'KAT-uh-list', 'ক্যাট-আ-লিস্ট', 'A person or thing that precipitates an event or change.', 'অনুঘটক বা পরিবর্তন সূচনাকারী', ['stimulant', 'spark', 'impetus'], ['inhibitor', 'obstacle', 'hindrance']),
    48: ('adjective', 'KAW-stik', 'কস-টিক', 'Sarcastic in a scathing and bitter way; corrosive.', 'তীক্ষ্ণ বা ব্যঙ্গাত্মক', ['sarcastic', 'scathing', 'mordant'], ['kind', 'gentle', 'soothing']),
    49: ('noun', 'shih-KAY-nuh-ree', 'শি-কেই-না-রি', 'The use of trickery or deception to achieve a purpose.', 'প্রতারণা বা চাতুর্য', ['trickery', 'deceit', 'subterfuge'], ['honesty', 'candor', 'integrity']),
    50: ('verb', 'koh-AG-yuh-layt', 'কো-অ্যাগ-ইউ-লেইট', 'To change from a liquid to a thickened or solid state; clot.', 'জমাট বাঁধা বা ঘন হওয়া', ['clot', 'solidify', 'curdle'], ['dissolve', 'liquefy', 'melt']),
    51: ('noun', 'KOH-duh', 'কো-ডা', 'A concluding event, remark, or musical section.', 'উপসংহার বা সমাপ্তি অংশ', ['conclusion', 'epilogue', 'finale'], ['introduction', 'prelude', 'beginning']),
    52: ('adjective', 'kuh-MEN-ser-it', 'কা-মেন-সার-ইট', 'Corresponding in size, extent, or degree; proportionate.', 'সমানুপাতিক বা সামঞ্জস্যপূর্ণ', ['proportionate', 'equal', 'equivalent'], ['disproportionate', 'unequal', 'incommensurate']),
    53: ('noun', 'kum-PEN-dee-um', 'কাম-পেন-ডি-আম', 'A concise collection of information or a comprehensive summary.', 'সারসংক্ষেপ বা সংক্ষিপ্ত সংকলন', ['summary', 'digest', 'compilation'], ['expansion', 'elaboration', 'enlargement']),
    54: ('adjective', 'kum-PLAY-sunt', 'কাম-প্লেই-স্যান্ট', 'Willing to please others; obliging or overly agreeable.', 'পরকে খুশি করতে আগ্রহী বা বাধ্য', ['obliging', 'accommodating', 'agreeable'], ['uncooperative', 'stubborn', 'defiant']),
    55: ('adjective', 'kum-PLY-unt', 'কাম-প্লাই-অ্যান্ট', 'Disposed to agree with others or obey rules; submissive.', 'অনুবর্তী বা আজ্ঞাবহ', ['obedient', 'submissive', 'tractable'], ['rebellious', 'defiant', 'obstinate']),
    56: ('adjective', 'kun-SIL-ee-uh-tor-ee', 'কান-সিল-ই-আ-টরি', 'Intended or likely to placate, appease, or pacify.', 'মিটমাটকারী বা আপসকামিতা প্রকাশক', ['pacifying', 'appeasing', 'placatory'], ['antagonistic', 'hostile', 'provocative']),
    57: ('verb', 'kun-DOHN', 'কান-ডোন', 'To accept, overlook, or allow morally questionable behavior.', 'উপেক্ষা করা বা ক্ষমা চোখে দেখা', ['overlook', 'forgive', 'excuse'], ['condemn', 'punish', 'denounce']),
    58: ('verb', 'kun-FOWND', 'কান-ফাউন্ড', 'To cause surprise, confusion, or bewilderment in.', 'হতভম্ব বা বিভ্রান্ত করা', ['confuse', 'perplex', 'baffle'], ['clarify', 'explain', 'enlighten']),
    59: ('noun', 'kon-uh-SUR', 'কন-আ-সার', 'An expert judge in matters of taste or the fine arts.', 'রসিক বা অভিজ্ঞ সমঝদার', ['expert', 'critic', 'aficionado'], ['novice', 'amateur', 'ignoramus']),
    60: ('adjective', 'KOH-junt', 'কো-জ্যান্ট', 'Clear, logical, and convincing; compelling.', 'অকাট্য বা যুক্তিযুক্ত', ['convincing', 'compelling', 'persuasive'], ['unconvincing', 'weak', 'invalid']),

    # Set 4 (61-80)
    61: ('noun', 'kun-TEN-shun', 'কান-টেন-শান', 'Heated disagreement or an assertion maintained in an argument.', 'বিতর্ক বা প্রতিদ্বন্দ্বিতা', ['dispute', 'conflict', 'argument'], ['agreement', 'harmony', 'concord']),
    62: ('adjective', 'kun-TEN-shus', 'কান-টেন-শাস', 'Causing or likely to cause an argument; controversial; quarrelsome.', 'ঝগড়াটে বা বিতর্কিত', ['quarrelsome', 'argumentative', 'disputatious'], ['peaceable', 'agreeable', 'conciliatory']),
    63: ('adjective', 'kun-TRYT', 'কান-ট্রাইট', 'Feeling or expressing remorse or penitence; deeply sorrowful for sin.', 'অনুতপ্ত বা অনুশোচনাদগ্ধ', ['remorseful', 'penitent', 'repentant'], ['unrepentant', 'defiant', 'shameless']),
    64: ('noun', 'kuh-NUN-drum', 'কা-নান-ড্রাম', 'A confusing and difficult problem or question; riddle.', 'জটিল ধাঁধা বা বিষম সমস্যা', ['puzzle', 'riddle', 'enigma'], ['solution', 'answer', 'clarity']),
    65: ('verb', 'kun-VURJ', 'কান-ভার্জ', 'To tend to meet at an intersecting point; come together.', 'একই বিন্দুতে মিলিত হওয়া', ['intersect', 'meet', 'unite'], ['diverge', 'separate', 'scatter']),
    66: ('adjective', 'KON-vuh-loo-tid', 'কন-ভা-লু-টিড', 'Extremely complex and difficult to follow; intricately twisted.', 'জটিল বা পেঁচানো', ['intricate', 'complex', 'tangled'], ['simple', 'straightforward', 'direct']),
    67: ('adjective', 'KRAY-vun', 'ক্রেই-ভান', 'Contemptibly lacking in courage; cowardly.', 'কাপুরুষোচিত বা ভীরু', ['cowardly', 'fainthearted', 'pusillanimous'], ['brave', 'courageous', 'valiant']),
    68: ('verb', 'DAWNT', 'ডন্ট', 'To make someone feel intimidated, discouraged, or apprehensive.', 'ভীত বা নিরুৎসাহিত করা', ['intimidate', 'discourage', 'dishearten'], ['encourage', 'embolden', 'inspire']),
    69: ('noun', 'dih-KOR-um', 'ডি-কর-আম', 'Behavior in keeping with good taste and propriety; etiquette.', 'শোভনতা বা ভদ্রোচিত আচরণ', ['propriety', 'etiquette', 'decency'], ['impropriety', 'indecency', 'rudeness']),
    70: ('noun', 'dih-FAWLT', 'ডি-ফল্ট', 'Failure to fulfill an obligation, especially to repay a loan.', 'দায় শোধে ব্যর্থতা বা অনুপস্থিতি', ['failure', 'nonpayment', 'delinquency'], ['compliance', 'fulfillment', 'payment']),
    71: ('noun', 'DEF-er-unss', 'ডিফ-এর-অ্যান্স', 'Polite submission and respect toward another’s wishes or judgment.', 'শ্রদ্ধাপূর্ণ সম্মতি বা সম্মান প্রদর্শন', ['respect', 'reverence', 'compliance'], ['disrespect', 'defiance', 'contempt']),
    72: ('verb', 'dih-LIN-ee-ayt', 'ডি-লিন-ই-এইট', 'To describe, portray, or outline precisely.', 'সুস্পষ্টভাবে বর্ণনা বা রূপরেখা দেওয়া', ['describe', 'outline', 'portray'], ['distort', 'confuse', 'obscure']),
    73: ('verb', 'DEN-ih-grayt', 'ডেন্স-ই-গ্রেইট', 'To criticize unfairly; disparage the character or reputation of.', 'মর্যাদাহানি করা বা ছোট করা', ['disparage', 'belittle', 'malign'], ['praise', 'extol', 'honor']),
    74: ('verb', 'dih-RYD', 'ডি-রাইড', 'To express contempt for; ridicule or mock.', 'উপহাস বা বিদ্রূপ করা', ['mock', 'ridicule', 'taunt'], ['praise', 'respect', 'admire']),
    75: ('adjective', 'dih-RIV-uh-tiv', 'ডি-রিভ-আ-টিভ', 'Imitative of the work of another; unoriginal.', 'মৌলিকতাহীন বা অনুকরণমূলক', ['unoriginal', 'imitative', 'copied'], ['original', 'innovative', 'novel']),
    76: ('verb', 'DES-ih-kayt', 'ডেস-ই-কেইট', 'To remove the moisture from; dry out completely.', 'সম্পূর্ণরূপে শুকানো বা আর্দ্রতাহীন করা', ['dry', 'dehydrate', 'drain'], ['hydrate', 'moisten', 'drench']),
    77: ('adjective', 'DES-ul-tor-ee', 'ডেস-আল-টরি', 'Lacking a plan, purpose, or enthusiasm; jumping from one thing to another.', 'এলোমেলো বা উদ্দেশ্যহীন', ['aimless', 'erratic', 'disconnected'], ['systematic', 'methodical', 'focused']),
    78: ('noun', 'dih-TUR-unt', 'ডি-টার-অ্যান্ট', 'A thing that discourages or is intended to discourage someone from doing something.', 'নিবারক বা প্রতিবন্ধক বস্তু', ['discouragement', 'obstacle', 'restraint'], ['incentive', 'encouragement', 'stimulus']),
    79: ('noun', 'DY-uh-tryb', 'ডাই-আ-ট্রাইব', 'A forceful and bitter verbal attack against someone or something.', 'তীব্র আক্রমণাত্মক বক্তৃতা বা ভর্ৎসনা', ['tirade', 'rant', 'invective'], ['praise', 'eulogy', 'encomium']),
    80: ('noun', 'dy-KOT-uh-mee', 'ডাই-কট-আ-মি', 'A division or contrast between two things represented as entirely opposing.', 'দ্বিধাবিভক্তি বা পরস্পরবিরোধী বিভাজন', ['division', 'split', 'contrast'], ['unity', 'harmony', 'union']),

    # Set 5 (81-100)
    81: ('noun', 'DIF-ih-dunss', 'ডিফ-ই-ড্যান্স', 'Modesty or shyness resulting from a lack of self-confidence.', 'আত্মবিশ্বাসের অভাব বা দ্বিধাগ্রস্ততা', ['shyness', 'timidity', 'hesitancy'], ['confidence', 'boldness', 'assurance']),
    82: ('adjective', 'dih-FYOOS', 'ডি-ফিউস', 'Spread out over a large area; wordy and lacking conciseness.', 'বিস্তৃত বা অসংহত ও দীর্ঘভাষী', ['scattered', 'verbose', 'dispersed'], ['concentrated', 'compact', 'concise']),
    83: ('noun', 'dy-GRESH-un', 'ডাই-গ্রেশ-আন', 'A temporary departure from the main subject in speech or writing.', 'মূল বিষয় থেকে বিচ্যুতি বা অপ্রাসঙ্গিক কথা', ['departure', 'deviation', 'divergence'], ['focus', 'coherence', 'directness']),
    84: ('noun', 'DURJ', 'ডার্জ', 'A mournful song, piece of music, or poem lamenting the dead.', 'শোকগীতি বা অন্ত্যেষ্টিক্রিয়ার সুর', ['lament', 'elegy', 'requiem'], ['celebration', 'ode', 'hymn']),
    85: ('verb', 'dis-uh-BYOOZ', 'ডিস-আ-বিউজ', 'To persuade someone that an idea or belief is mistaken; disillusion.', 'ভুল ধারণা বা মোহ ভেঙে দেওয়া', ['disillusion', 'undeceive', 'correct'], ['deceive', 'mislead', 'delude']),
    86: ('adjective', 'dih-SURN-ing', 'ডি-সার্ন-ইং', 'Having or showing good judgment and acute insight.', 'সূক্ষ্মদর্শী বা বিচারবুদ্ধিসম্পন্ন', ['perceptive', 'insightful', 'astute'], ['undiscriminating', 'obtuse', 'unperceptive']),
    87: ('adjective', 'dis-KOR-dunt', 'ডিস-কর-ড্যান্ট', 'Disagreeing or incongruous; harsh and jarring because of lack of harmony.', 'বেসুরো বা অমিলযুক্ত', ['inharmonious', 'dissonant', 'conflicting'], ['harmonious', 'agreeable', 'consonant']),
    88: ('verb', 'dis-KRED-it', 'ডিস-ক্রেড-ইট', 'To harm the good reputation of; cause an idea to seem untrue.', 'মর্যাদা ক্ষুণ্ণ করা বা অবিশ্বাসযোগ্য করা', ['disprove', 'disparage', 'undermine'], ['validate', 'endorse', 'confirm']),
    89: ('noun', 'dis-KREP-un-see', 'ডিস-ক্রেপ-আন-সি', 'A lack of compatibility or similarity between two or more facts; discrepancy.', 'অমিল বা গরমিল', ['inconsistency', 'divergence', 'variance'], ['consistency', 'similarity', 'agreement']),
    90: ('adjective', 'dih-SKREET', 'ডি-স্ক্রিট', 'Individually separate, distinct, and detached.', 'স্বতন্ত্র বা পৃথক', ['separate', 'distinct', 'isolated'], ['connected', 'continuous', 'integrated']),
    91: ('adjective', 'dis-in-JEN-yoo-us', 'ডিস-ইন-জেন-ইউ-আস', 'Not candid or sincere, typically by pretending to know less than one does.', 'কপট বা অসৎ উদ্দেশ্যপ্রণোদিত', ['insincere', 'deceitful', 'duplicitous'], ['candid', 'sincere', 'frank']),
    92: ('adjective', 'dis-IN-ter-est-id', 'ডিস-ইন-টার-এস্ট-ইড', 'Not influenced by personal interest or selfish motive; impartial.', 'পক্ষপাতহীন বা নির্লিপ্ত', ['impartial', 'unbiased', 'objective'], ['biased', 'partial', 'prejudiced']),
    93: ('adjective', 'dis-JOYN-tid', 'ডিস-জয়ন-টিড', 'Lacking a coherent sequence or connection; incoherent.', 'অসংলগ্ন বা বিচ্ছিন্ন', ['disconnected', 'fragmented', 'incoherent'], ['coherent', 'connected', 'unified']),
    94: ('verb', 'dis-MIS', 'ডিস-মিস', 'To treat as unworthy of serious consideration; discard.', 'উড়িয়ে দেওয়া বা নাকচ করা', ['reject', 'disregard', 'spurn'], ['accept', 'consider', 'embrace']),
    95: ('verb', 'dih-SPAR-ij', 'ডি-স্প্যার-ইজ', 'To regard or represent as being of little worth; belittle.', 'অবমূল্যায়ন করা বা তাচ্ছিল্য করা', ['belittle', 'depreciate', 'deride'], ['praise', 'extol', 'appreciate']),
    96: ('adjective', 'DIS-per-it', 'ডিস-পার-ইট', 'Essentially different in kind; not allowing comparison.', 'একেবারে ভিন্ন বা বৈসাদৃশ্যপূর্ণ', ['dissimilar', 'divergent', 'unrelated'], ['similar', 'identical', 'alike']),
    97: ('verb', 'dih-SEM-bul', 'ডি-সেম-বাল', 'To conceal one’s true motives, feelings, or beliefs; pretend.', 'মনোভাব গোপন করা বা ভান করা', ['disguise', 'feign', 'mask'], ['reveal', 'manifest', 'disclose']),
    98: ('verb', 'dih-SEM-uh-nayt', 'ডি-সেম-আ-নেইট', 'To spread or disperse widely, especially news or information.', 'ব্যাপকভাবে ছড়িয়ে দেওয়া বা প্রচার করা', ['spread', 'circulate', 'disperse'], ['gather', 'collect', 'withhold']),
    99: ('noun', 'dis-uh-LOO-shun', 'ডিস-আ-লু-শান', 'The closing down, disintegration, or dismissal of an official body.', 'ভেঙে দেওয়া বা অবলুপ্তি', ['disintegration', 'termination', 'breakup'], ['creation', 'formation', 'union']),
    100: ('noun', 'DIS-uh-nunss', 'ডিস-আ-ন্যান্স', 'A lack of harmony among musical notes or disagreement between people.', 'সুরবিরোধ বা অসঙ্গতি', ['discord', 'disharmony', 'conflict'], ['harmony', 'consonance', 'accord']),

    # Set 6 (101-120)
    101: ('verb', 'dih-STEND', 'ডি-স্টেন্ড', 'To swell, expand, or bloat from internal pressure.', 'স্ফীত বা প্রসারিত হওয়া', ['swell', 'expand', 'bloat'], ['shrink', 'contract', 'deflate']),
    102: ('verb', 'dih-STIL', 'ডি-স্টিল', 'To extract the essential meaning or purest elements of.', 'পরিশোধন করা বা সারমর্ম বের করা', ['purify', 'refine', 'concentrate'], ['pollute', 'contaminate', 'dilute']),
    103: ('verb', 'dy-VURJ', 'ডাই-ভার্জ', 'To separate from another route, move in a different direction; deviate.', 'ভিন্নমুখী হওয়া বা অপসারিত হওয়া', ['deviate', 'separate', 'branch'], ['converge', 'merge', 'unite']),
    104: ('verb', 'dy-VEST', 'ডাই-ভেস্ট', 'To strip or deprive someone of power, rights, or possessions.', 'বঞ্চিত করা বা প্রত্যাহার করা', ['strip', 'deprive', 'dispossess'], ['invest', 'endow', 'grant']),
    105: ('verb', 'DOK-yuh-ment', 'ডক-ইউ-মেন্ট', 'To record, support, or substantiate with evidence.', 'দলিলবদ্ধ করা বা প্রমাণসহ নথিবদ্ধ করা', ['record', 'verify', 'substantiate'], ['disprove', 'ignore', 'fabricate']),
    106: ('adjective', 'dog-MAT-ik', 'ডগ-ম্যাট-ইক', 'Inclined to lay down principles as incontrovertibly true without evidence.', 'গোঁড়া বা অন্ধ মতবাদী', ['authoritarian', 'doctrinaire', 'inflexible'], ['open-minded', 'flexible', 'pragmatic']),
    107: ('adjective', 'DOR-munt', 'ডর-ম্যান্ট', 'Having normal physical functions suspended or slowed down; inactive.', 'সুপ্ত বা নিষ্ক্রিয়', ['inactive', 'quiescent', 'latent'], ['active', 'awake', 'operative']),
    108: ('verb', 'DOOP', 'ডুপ', 'To deceive or trick someone easily.', 'প্রতারিত করা বা বোকা বানানো', ['deceive', 'trick', 'swindle'], ['enlighten', 'protect', 'guide']),
    109: ('adjective', 'ih-BOOL-yunt', 'ই-বুল-ই-অ্যান্ট', 'Cheerful, enthusiastic, and full of high energy; exuberant.', 'উচ্ছ্বসিত বা প্রাণোচ্ছ্বল', ['exuberant', 'enthusiastic', 'vivacious'], ['depressed', 'gloomy', 'apathetic']),
    110: ('adjective', 'eh-KLEK-tik', 'এক-লেক-টিক', 'Deriving ideas, style, or taste from a broad and diverse range of sources.', 'বিভিন্ন উৎস থেকে সংগৃহীত বা বহুমাত্রিক', ['diverse', 'varied', 'multifaceted'], ['narrow', 'uniform', 'specialized']),
    111: ('noun', 'EF-ih-kuh-see', 'এফ-ই-কা-সি', 'The ability to produce a desired or intended result; effectiveness.', 'কার্যকারিতা বা কার্যক্ষমতা', ['effectiveness', 'potency', 'success'], ['inefficacy', 'ineffectiveness', 'uselessness']),
    112: ('noun', 'eh-FRUN-tuh-ree', 'এফ-রান-টা-রি', 'Insolent or impertinent behavior; shameless audacity.', 'অহংকারী ধৃষ্টতা বা চরম ঔদ্ধত্য', ['audacity', 'impertinence', 'insolence'], ['timidity', 'respect', 'modesty']),
    113: ('noun', 'EL-uh-jee', 'এল-আ-জি', 'A poem of serious reflection, typically a mournful lament for the dead.', 'শোকগাথা বা বিলাপকাব্য', ['lament', 'dirge', 'requiem'], ['panegyric', 'tribute', 'celebration']),
    114: ('verb', 'ih-LIS-it', 'ই-লিস-ইট', 'To evoke, draw out, or provoke a response or reaction.', 'প্রকাশিত করা বা টেনে বের করা', ['evoke', 'extract', 'obtain'], ['suppress', 'hide', 'repress']),
    115: ('verb', 'em-BEL-ish', 'এম-বেল-ইশ', 'To make more attractive by adding decorative details or features.', 'সজ্জিত বা সুন্দর করা', ['decorate', 'adorn', 'enhance'], ['mar', 'deface', 'spoil']),
    116: ('adjective', 'em-PEER-ih-kul', 'এম-পির-ই-কাল', 'Based on, concerned with, or verifiable by observation or experiment.', 'অভিজ্ঞতালব্ধ বা পর্যবেক্ষণভিত্তিক', ['experimental', 'practical', 'observed'], ['theoretical', 'hypothetical', 'speculative']),
    117: ('verb', 'EM-yuh-layt', 'এম-ইউ-লেইট', 'To match or surpass a person or achievement, typically by imitation.', 'অনুকরণ করা বা সমকক্ষ হতে চেষ্টা করা', ['imitate', 'copy', 'mirror'], ['originate', 'neglect', 'diverge']),
    118: ('adjective', 'en-DEM-ik', 'এন-ডেম-ইক', 'Regularly found among particular people or restricted to a certain area.', 'নির্দিষ্ট স্থান বা জনগোষ্ঠীর মধ্যে সীমাবদ্ধ', ['native', 'indigenous', 'local'], ['exotic', 'foreign', 'pandemic']),
    119: ('verb', 'EN-er-vayt', 'এন-এর-ভেইট', 'To cause someone to feel drained of energy or vitality; weaken.', 'দুর্বল বা শক্তিহীন করা', ['weaken', 'exhaust', 'debilitate'], ['energize', 'strengthen', 'invigorate']),
    120: ('verb', 'en-JEN-der', 'এন-জেন-ডার', 'To cause, create, or give rise to a feeling or situation.', 'সৃষ্টি করা বা জন্ম দেওয়া', ['produce', 'generate', 'cause'], ['destroy', 'quash', 'extinguish']),

    # Set 7 (121-140)
    121: ('verb', 'en-HANSS', 'এন-হ্যান্স', 'To intensify, increase, or further improve the quality or value of.', 'বৃদ্ধি করা বা মান উন্নত করা', ['improve', 'boost', 'upgrade'], ['diminish', 'impair', 'reduce']),
    122: ('adjective', 'ih-FEM-er-ul', 'ই-ফেম-এর-আল', 'Lasting for a very short time; transitory; fleeting.', 'ক্ষণস্থায়ী বা স্বল্পজীবী', ['transitory', 'fleeting', 'momentary'], ['permanent', 'eternal', 'perpetual']),
    123: ('noun', 'ek-wuh-NIM-ih-tee', 'এক-ওয়া-নিম-ই-টি', 'Mental calmness, composure, and evenness of temper in difficulty.', 'মনের স্থিরতা বা অবিচল মানসিক প্রশান্তি', ['composure', 'calmness', 'serenity'], ['agitation', 'anxiety', 'hysteria']),
    124: ('verb', 'ih-KWIV-uh-kayt', 'ই-কুইভ-আ-কেইট', 'To use ambiguous language so as to conceal the truth or avoid commitment.', 'দ্ব্যর্থবোধক কথা বলা বা স্পষ্ট এড়িয়ে যাওয়া', ['prevaricate', 'hedge', 'dodge'], ['confront', 'clarify', 'declare']),
    125: ('adjective', 'ER-yoo-dyt', 'এর-ইউ-ডাইট', 'Having or showing great knowledge or learning; scholarly.', 'পণ্ডিত বা বিদ্যান', ['scholarly', 'learned', 'knowledgeable'], ['ignorant', 'illiterate', 'unscholarly']),
    126: ('adjective', 'es-uh-TARE-ik', 'এস-আ-টের-ইক', 'Intended for or understood by only a small group with specialized knowledge.', 'গূঢ় বা গুহ্য বিষয় সম্পর্কিত', ['abstruse', 'obscure', 'arcane'], ['obvious', 'public', 'common']),
    127: ('noun', 'YOO-luh-jee', 'ইউ-লা-জি', 'A speech or writing that praises someone highly, typically deceased.', 'প্রশংসাসূচক ভাষণ বা স্তুতিগাথা', ['praise', 'accolade', 'encomium'], ['diatribe', 'condemnation', 'criticism']),
    128: ('noun', 'YOO-fuh-miz-um', 'ইউ-ফা-মিজ-ম', 'A mild or indirect expression substituted for one considered too blunt.', 'শ্রুতিকটু শব্দের পরিবর্তে মধুর শব্দের প্রয়োগ', ['polite term', 'understatement', 'softener'], ['dysphemism', 'harshness', 'bluntness']),
    129: ('verb', 'ig-ZAS-er-bayt', 'ইগ-জ্যাস-এর-বেইট', 'To make a problem, bad situation, or negative feeling worse.', 'আরও খারাপ বা অবনতি করা', ['worsen', 'aggravate', 'intensify'], ['alleviate', 'soothe', 'improve']),
    130: ('verb', 'EK-skul-payt', 'এক-স্কাল-পেইট', 'To show or declare that someone is not guilty of wrongdoing; exonerate.', 'দোষমুক্ত বা নির্দোষ প্রমাণিত করা', ['exonerate', 'absolve', 'acquit'], ['incriminate', 'condemn', 'convict']),
    131: ('noun', 'EK-sih-jun-see', 'এক-সি-জান-সি', 'An urgent need or demand; an emergency situation requiring action.', 'জরুরি অবস্থা বা আশু প্রয়োজন', ['urgency', 'crisis', 'emergency'], ['calm', 'leisure', 'ease']),
    132: ('noun', 'ek-strap-uh-LAY-shun', 'এক-স্ট্র্যাপ-আ-লেই-শান', 'An estimation of a value based on extending known data or trends.', 'জানা তথ্যের ভিত্তিতে দূরবর্তী অনুমান', ['projection', 'estimation', 'deduction'], ['measurement', 'fact', 'certainty']),
    133: ('adjective', 'fuh-SEE-shus', 'ফা-সি-শাস', 'Treating serious issues with deliberately inappropriate humor; flippant.', 'লঘুচাপল্যপূর্ণ বা ঠাট্টাপূর্ণ', ['flippant', 'humorous', 'jocular'], ['serious', 'grave', 'somber']),
    134: ('verb', 'fuh-SIL-ih-tayt', 'ফা-সিল-ই-তেইট', 'To make an action or process easy or easier.', 'সহজতর বা সুগম করা', ['ease', 'assist', 'expedite'], ['hinder', 'impede', 'obstruct']),
    135: ('adjective', 'fuh-LAY-shus', 'ফা-লেই-শাস', 'Based on a mistaken belief or unsound reasoning; deceptive.', 'ভ্রান্ত বা বিভ্রান্তিকর', ['misleading', 'deceptive', 'erroneous'], ['truthful', 'valid', 'accurate']),
    136: ('adjective', 'FACH-oo-us', 'ফ্যাচ-উ-আস', 'Silly, pointless, and foolish in a self-satisfied manner.', 'নির্বোধ বা বুদ্ধিহীন', ['foolish', 'silly', 'inane'], ['sensible', 'wise', 'intelligent']),
    137: ('adjective', 'FAWN-ing', 'ফন-ইং', 'Displaying exaggerated flattery or affection; obsequious.', 'তোষামোদকারী বা চাটুকারপূর্ণ', ['sycophantic', 'obsequious', 'flattering'], ['aloof', 'critical', 'disdainful']),
    138: ('adjective', 'fih-LIS-ih-tus', 'ফি-লিস-ই-টাস', 'Well chosen or suited to the circumstances; pleasing and fortunate.', 'যথোপযুক্ত বা সুখকর', ['appropriate', 'apt', 'fitting'], ['inappropriate', 'unfortunate', 'inept']),
    139: ('noun', 'FUR-ver', 'ফার-ভার', 'Intense and passionate feeling; great warmth of emotion.', 'অত্যধিক উদ্দীপনা বা আন্তরিক তীব্রতা', ['passion', 'ardor', 'zeal'], ['apathy', 'indifference', 'coolness']),
    140: ('verb', 'FLAG', 'ফ্ল্যাগ', 'To become tired, weaker, or less enthusiastic; droop.', 'ক্লান্ত হওয়া বা তেজ হ্রাস পাওয়া', ['droop', 'weaken', 'wane'], ['revive', 'strengthen', 'flourish']),

    # Set 8 (141-160)
    141: ('noun', 'FLEJ-ling', 'ফ্লেজ-লিং', 'A person, organization, or project that is newly established or inexperienced.', 'অনভিজ্ঞ ব্যক্তি বা নতুন কোনো উদ্যোগ', ['novice', 'beginner', 'rookie'], ['veteran', 'expert', 'master']),
    142: ('verb', 'FLOWT', 'ফ্লাউট', 'To openly disregard a rule, law, or convention with contempt.', 'আইন বা নিয়ম অগ্রাহ্য করা', ['defy', 'scorn', 'disregard'], ['obey', 'respect', 'comply']),
    143: ('verb', 'foh-MENT', 'ফো-মেন্ট', 'To instigate or stir up violent or rebellious sentiment.', 'উস্কানি দেওয়া বা প্ররোচিত করা', ['instigate', 'incite', 'provoke'], ['quell', 'suppress', 'dampen']),
    144: ('verb', 'for-STAWL', 'ফর-স্টল', 'To prevent or obstruct an anticipated event by taking action ahead of time.', 'আগাম ব্যবস্থা নিয়ে প্রতিহত করা', ['preempt', 'prevent', 'thwart'], ['facilitate', 'permit', 'encourage']),
    145: ('noun', 'froo-GAL-ih-tee', 'ফ্রু-গ্যাল-ই-টি', 'The quality of being economical with money or food; thriftiness.', 'মিতব্যয়িতা বা হিসেবি স্বভাব', ['thrift', 'economy', 'providence'], ['extravagance', 'wastefulness', 'prodigality']),
    146: ('adjective', 'FYOO-tul', 'ফিউ-টাইল', 'Incapable of producing any useful result; pointless or vain.', 'ব্যর্থ বা নিষ্ফল', ['pointless', 'useless', 'vain'], ['useful', 'effective', 'fruitful']),
    147: ('verb', 'gayn-SAY', 'গেইন-সেই', 'To deny, contradict, or speak against a fact or statement.', 'অস্বীকার করা বা প্রতিবাদ করা', ['contradict', 'deny', 'dispute'], ['admit', 'confirm', 'agree']),
    148: ('adjective', 'GAIR-uh-lus', 'গ্যার-আ-লাস', 'Excessively talkative, especially on trivial matters; loquacious.', 'বাচাল বা অতিভাষী', ['talkative', 'loquacious', 'voluble'], ['taciturn', 'reticent', 'concise']),
    149: ('verb', 'GOHD', 'গোড', 'To provoke or annoy someone so as to stimulate action or reaction.', 'উত্তেজিত করা বা তাড়িয়ে নিয়ে যাওয়া', ['provoke', 'spur', 'prod'], ['deter', 'restrain', 'dissuade']),
    150: ('verb', 'GOWJ', 'গাউজ', 'To overcharge someone exorbitantly or swindle.', 'অতিরিক্ত দাম নেওয়া বা প্রতারণা করা', ['overcharge', 'swindle', 'exploit'], ['undercharge', 'discount', 'refund']),
    151: ('adjective', 'gran-DIL-uh-kwunt', 'গ্র্যান-ডিল-আ-কোয়ান্ট', 'Pompous or extravagant in language, style, or manner.', 'বাগাড়ম্বরপূর্ণ বা জাঁকালো কথার স্বভাব', ['bombastic', 'pretentious', 'pompous'], ['simple', 'plainspoken', 'modest']),
    152: ('adjective', 'grih-GAIR-ee-us', 'গ্রি-গের-ই-আস', 'Fond of company; sociable and enjoying being around others.', 'মিশুক বা দলবদ্ধ থাকতে পছন্দকারী', ['sociable', 'outgoing', 'companionable'], ['reclusive', 'unsociable', 'solitary']),
    153: ('adjective', 'GYL-lis', 'গাইল-লেস', 'Devoid of guile; completely innocent and without deception.', 'অকপট বা নিষ্পাপ ও সরল', ['innocent', 'naive', 'honest'], ['deceitful', 'cunning', 'crafty']),
    154: ('adjective', 'GUL-uh-bul', 'গাল-আ-বাল', 'Easily persuaded to believe something; credulous and easily tricked.', 'অতিবিশ্বাসপ্রবণ বা সহজেই ধোঁকা খায় এমন', ['credulous', 'trusting', 'naive'], ['skeptical', 'shrewd', 'suspicious']),
    155: ('noun', 'huh-RANG', 'হা-র্যাং', 'A lengthy and aggressive speech or lecture; tirade.', 'উত্তেজনাপূর্ণ বা আক্রমণাত্মক দীর্ঘ বক্তৃতা', ['tirade', 'diatribe', 'lecture'], ['tribute', 'accolade', 'whisper']),
    156: ('adjective', 'hoh-muh-JEE-nee-us', 'হো-মা-জি-নি-আস', 'Of the same kind; alike in composition throughout.', 'সমজাতীয় বা সমরূপ', ['uniform', 'consistent', 'identical'], ['heterogeneous', 'varied', 'diverse']),
    157: ('noun', 'hy-PUR-buh-lee', 'হাই-পার-বা-লি', 'Exaggerated statements or claims not meant to be taken literally.', 'অতিরঞ্জন বা অত্যুক্তি', ['exaggeration', 'overstatement', 'magnification'], ['understatement', 'litotes', 'reality']),
    158: ('adjective', 'eye-kon-uh-KLAS-tik', 'আই-কন-আ-ক্ল্যাস-টিক', 'Characterized by attack on cherished beliefs or established institutions.', 'প্রথাভাঙ্গা বা সনাতন আদর্শের বিরোধী', ['rebellious', 'subversive', 'unconventional'], ['traditional', 'orthodox', 'conformist']),
    159: ('noun', 'eye-DOL-uh-tree', 'আই-ডল-আ-ট্রি', 'Extreme admiration, worship, or blind reverence for something or someone.', 'অন্ধ ভক্তি বা অন্ধপূজা', ['worship', 'adoration', 'veneration'], ['disdain', 'scorn', 'contempt']),
    160: ('adjective', 'ih-MYOO-tuh-bul', 'ই-মিউ-টা-বাল', 'Unchanging over time or unable to be changed; constant.', 'অপরিবর্তনীয় বা চিরন্তন', ['unchangeable', 'fixed', 'permanent'], ['changeable', 'variable', 'mutable']),

    # Set 9 (161-180)
    161: ('verb', 'im-PAIR', 'ইম-পেয়ার', 'To weaken, damage, or diminish in strength or quality.', 'ক্ষতিগ্রস্ত বা দুর্বল করা', ['damage', 'weaken', 'diminish'], ['improve', 'enhance', 'repair']),
    162: ('adjective', 'im-PAS-iv', 'ইম-প্যাস-ইভ', 'Not feeling or showing emotion; calm and expressionless.', 'ভাবলেশহীন বা আবেগহীন', ['stoic', 'expressionless', 'unemotional'], ['expressive', 'emotional', 'passionate']),
    163: ('verb', 'im-PEED', 'ইম-পীড', 'To delay or prevent someone or something by obstructing them; hinder.', 'বাধা দেওয়া বা ব্যাহত করা', ['hinder', 'obstruct', 'hamper'], ['facilitate', 'assist', 'expedite']),
    164: ('adjective', 'im-PUR-mee-uh-bul', 'ইম-পার-মি-আ-বাল', 'Not allowing fluid or gas to pass through; impervious.', 'অভেদ্য বা অপ্রবেশ্য', ['impenetrable', 'waterproof', 'impervious'], ['permeable', 'porous', 'absorbent']),
    165: ('adjective', 'im-per-TUR-buh-bul', 'ইম-পার-টার-বা-বাল', 'Unable to be upset or excited; staying calm and cool.', 'শান্ত বা সহজে বিচলিত হয় না এমন', ['unflappable', 'serene', 'calm'], ['excitable', 'jittery', 'anxious']),
    166: ('adjective', 'im-PUR-vee-us', 'ইম-পার-ভি-আস', 'Unable to be affected by; not allowing entrance or penetration.', 'অপ্রভাবিত বা অভেদ্য', ['impermeable', 'immune', 'resistant'], ['vulnerable', 'susceptible', 'receptive']),
    167: ('adjective', 'im-PLAK-uh-bul', 'ইম-প্ল্যাক-আ-বাল', 'Unable to be placated, appeased, or pacified; relentless.', 'কঠোর বা ক্ষমাহীন ও অনমনীয়', ['unyielding', 'relentless', 'ruthless'], ['forgiving', 'pliable', 'merciful']),
    168: ('adjective', 'im-PLIS-it', 'ইম-প্লিস-ইট', 'Implied though not plainly expressed; absolute and unreserved.', 'অন্তর্নিহিত বা পরোক্ষ', ['implied', 'hinted', 'unspoken'], ['explicit', 'direct', 'stated']),
    169: ('verb', 'im-PLOHD', 'ইম-প্লোড', 'To collapse or cause to collapse violently inward.', 'ভেতরের দিকে ভেঙে পড়া বা চূর্ণ হওয়া', ['collapse', 'cave in', 'fall apart'], ['explode', 'expand', 'burst']),
    170: ('adverb', 'in-ad-VUR-tunt-lee', 'ইন-অ্যাড-ভার-টেন্ট-লি', 'Without intention; accidentally or carelessly.', 'অনিচ্ছাকৃতভাবে বা ভুলবশত', ['accidentally', 'unintentionally', 'mistakenly'], ['deliberately', 'intentionally', 'purposely']),
    171: ('adjective', 'in-KOH-it', 'ইন-কো-ইট', 'Just begun and so not fully formed or developed; rudimentary.', 'প্রাথমিক বা অপরিণত পর্যায়ের', ['rudimentary', 'undeveloped', 'incipient'], ['mature', 'developed', 'complete']),
    172: ('noun', 'in-kun-GROO-ih-tee', 'ইন-কান-গ্রু-ই-টি', 'The state of being out of place or inconsistent with surroundings.', 'অসঙ্গতি বা অনুপযুক্ততা', ['inappropriateness', 'mismatch', 'inconsistency'], ['suitability', 'harmony', 'appropriateness']),
    173: ('adjective', 'in-kon-sih-KWEN-shul', 'ইন-কন-সি-কোয়েন-শাল', 'Not important or significant; trivial.', 'তুচ্ছ বা গুরুত্বহীন', ['insignificant', 'trivial', 'minor'], ['significant', 'important', 'crucial']),
    174: ('verb', 'in-KOR-puh-rayt', 'ইন-কর-পা-রেইট', 'To take in or contain something as part of a whole; include.', 'অন্তর্ভুক্ত বা একীভূত করা', ['include', 'integrate', 'assimilate'], ['exclude', 'separate', 'omit']),
    175: ('adjective', 'in-dih-TUR-min-it', 'ইন-ডি-টার-মিন-ইট', 'Not exactly known, established, or defined; uncertain.', 'অনির্দিষ্ট বা অনিশ্চিত', ['uncertain', 'vague', 'unspecified'], ['definite', 'fixed', 'certain']),
    176: ('noun', 'IN-dih-junss', 'ইন-ডি-জ্যান্স', 'A state of extreme poverty; destitution.', 'চরম দারিদ্র্য বা নিঃস্ব অবস্থা', ['poverty', 'destitution', 'penury'], ['wealth', 'affluence', 'prosperity']),
    177: ('adjective', 'IN-duh-lunt', 'ইন-ডা-ল্যান্ট', 'Wanting to avoid activity or exertion; habitual laziness.', 'অলস বা কর্মবিমুখ', ['lazy', 'slothful', 'idle'], ['diligent', 'industrious', 'active']),
    178: ('adjective', 'ih-NURT', 'ই-নার্ট', 'Lacking the ability or strength to move; inactive.', 'নিষ্ক্রিয় বা জড়', ['motionless', 'inactive', 'dormant'], ['active', 'dynamic', 'lively']),
    179: ('adjective', 'in-JEN-yoo-us', 'ইন-জেন-ইউ-আস', 'Innocent and unsuspecting; naive and free from deceit.', 'সরল বা অকপট স্বভাবের', ['innocent', 'naive', 'artless'], ['cunning', 'deceitful', 'sophisticated']),
    180: ('adjective', 'in-HEER-unt', 'ইন-হির-অ্যান্ট', 'Existing in something as a permanent, essential, or characteristic attribute.', 'সহজাত বা স্বভাবজাত', ['intrinsic', 'innate', 'inborn'], ['extrinsic', 'acquired', 'alien']),

    # Set 10 (181-200)
    181: ('adjective', 'ih-NOK-yoo-us', 'ই-নক-ইউ-আস', 'Not harmful or offensive; harmless.', 'নিরপরাধ বা ক্ষতিকর নয় এমন', ['harmless', 'benign', 'safe'], ['harmful', 'toxic', 'dangerous']),
    182: ('adjective', 'in-SEN-sih-bul', 'ইন-সেন-সি-বাল', 'Incapable of physical sensation; unconscious or unaware.', 'অজ্ঞান বা অনুভূতিহীন', ['unconscious', 'numb', 'unaware'], ['conscious', 'aware', 'sensitive']),
    183: ('verb', 'in-SIN-yoo-ayt', 'ইন-সিন-ইউ-এইট', 'To suggest or hint at something bad in an indirect manner.', 'ইঙ্গিত করা বা পরোক্ষভাবে বলা', ['imply', 'hint', 'intimate'], ['declare', 'state directly', 'announce']),
    184: ('adjective', 'in-SIP-id', 'ইন-সিপ-ইড', 'Lacking flavor; lacking vigor or interest; dull.', 'স্বাদহীন বা নীরস', ['tasteless', 'bland', 'dull'], ['flavorful', 'exciting', 'piquant']),
    185: ('noun', 'in-suh-LAIR-ih-tee', 'ইন-সা-লের-ই-টি', 'Ignorance of or lack of interest in cultures outside one’s own; narrow-mindedness.', 'সংকীর্ণমনা দৃষ্টিভঙ্গি বা বিচ্ছিন্ন মনোভাব', ['parochialism', 'narrow-mindedness', 'provincialism'], ['broad-mindedness', 'cosmopolitanism', 'openness']),
    186: ('adjective', 'in-TRAK-tuh-bul', 'ইন-ট্র্যাক-টা-বাল', 'Hard to control, manage, or deal with; stubbornly stubborn.', 'অবাধ্য বা নিয়ন্ত্রণ করা কঠিন এমন', ['stubborn', 'unmanageable', 'obstinate'], ['manageable', 'compliant', 'tractable']),
    187: ('noun', 'in-TRAN-zih-junss', 'ইন-ট্র্যান-জি-জ্যান্স', 'Refusal to change one’s views or to agree about something; stubborn inflexibility.', 'অনমনীয়তা বা চরম আপসহীনতা', ['stubbornness', 'obstinacy', 'inflexibility'], ['flexibility', 'compliance', 'cooperation']),
    188: ('verb', 'IN-un-dayt', 'ইন-আন-ডেইট', 'To overwhelm someone with things or tasks; flood with water.', 'প্লাবিত করা বা বিপুল পরিমাণে চাপিয়ে দেওয়া', ['overwhelm', 'flood', 'swamp'], ['drain', 'underwhelm', 'starve']),
    189: ('adjective', 'ih-NYOORD', 'ই-নিউর্ড', 'Accustomed to someone or something, especially hardship or unpleasantness.', 'অভ্যস্ত বা সহনশীল হয়ে ওঠা', ['hardened', 'accustomed', 'habituated'], ['sensitive', 'unaccustomed', 'vulnerable']),
    190: ('noun', 'in-VEK-tiv', 'ইন-ভেক-টিভ', 'Insulting, abusive, or highly critical language.', 'তীব্র গালিগালাজ বা অপবাদমূলক বক্তব্য', ['abuse', 'insults', 'vituperation'], ['praise', 'accolade', 'compliment']),
    191: ('adjective', 'ih-RAS-uh-bul', 'ই-র্যাস-আ-বাল', 'Having or showing a tendency to be easily angered; quick-tempered.', 'বদমেজাজী বা খিটখিটে স্বভাবের', ['irritable', 'cantankerous', 'hot-tempered'], ['placid', 'calm', 'good-natured']),
    192: ('adjective', 'ih-REZ-uh-loot', 'ই-রেজ-আ-লুট', 'Showing or feeling hesitancy; uncertain; indecisive.', 'দ্বিধাগ্রস্ত বা অনিশ্চিত', ['indecisive', 'hesitant', 'wavering'], ['resolute', 'decisive', 'determined']),
    193: ('noun', 'eye-TIN-er-air-ee', 'আই-টিন-এর-এরি', 'A planned route or journey; detailed travel schedule.', 'ভ্রমণ পরিকল্পনা বা গতিসূচি', ['schedule', 'route', 'travel plan'], ['detour', 'randomness', 'spontaneity']),
    194: ('adjective', 'luh-KON-ik', 'লা-কন-ইক', 'Using very few words; concise; terse.', 'স্বল্পভাষী বা সংক্ষিপ্ত', ['concise', 'terse', 'succinct'], ['verbose', 'loquacious', 'garrulous']),
    195: ('noun', 'LAS-ih-tood', 'ল্যাস-ই-টুড', 'A state of physical or mental weariness; lack of energy.', 'ক্লান্তি বা অবসন্নতা', ['lethargy', 'sluggishness', 'fatigue'], ['vigor', 'energy', 'vitality']),
    196: ('adjective', 'LAY-tunt', 'লেই-ট্যান্ট', 'Existing but not yet developed or manifest; hidden or dormant.', 'সুপ্ত বা অপ্রকাশিত', ['hidden', 'dormant', 'underlying'], ['manifest', 'obvious', 'apparent']),
    197: ('verb', 'LAWD', 'লড', 'To praise a person or their achievements highly.', 'উচ্চ প্রশংসা করা বা গুণকীর্তন করা', ['praise', 'extol', 'commend'], ['criticize', 'condemn', 'censure']),
    198: ('adjective', 'luh-THAR-jik', 'লা-থার-জিক', 'Affected by sluggishness, drowsiness, and lack of energy.', 'অলস বা নিস্তেজ', ['sluggish', 'slothful', 'apathetic'], ['energetic', 'active', 'lively']),
    199: ('noun', 'LEV-ee', 'লেভ-ই', 'An embankment built to prevent the overflow of a river; floodbank.', 'নদীর বাঁধ বা বন্যা প্রতিরোধক প্রাচীর', ['embankment', 'dyke', 'barrier'], ['channel', 'trench', 'depression']),
    200: ('noun', 'LEV-ih-tee', 'লেভ-ই-টি', 'Treatment of a serious matter with humor; lack of appropriate seriousness.', 'লঘুচাপল্য বা দায়িত্বজ্ঞানহীন হাসিঠাট্টা', ['flippancy', 'lightheartedness', 'frivolity'], ['seriousness', 'gravity', 'solemnity'])
}

# Vowel sign deduplication and ligature correction for Bangla strings
def clean_bangla(text):
    if not text:
        return ''
    t = text
    # Deduplicate repeated vowel signs and diacritics
    t = re.sub(r'া+', 'া', t)
    t = re.sub(r'ী+', 'ী', t)
    t = re.sub(r'ূ+', 'ূ', t)
    t = re.sub(r'ঁ+', 'ঁ', t)
    t = re.sub(r'্+', '্', t)
    t = re.sub(r'ং+', 'ং', t)
    
    replacements = {
        'হ্রাাস': 'হ্রাস',
        'সতক': 'সতর্ক',
        'তিরস্কাার': 'তিরস্কার',
        'সৌন্দযবোধসম্পন্ন': 'সৌন্দর্যবোধসম্পন্ন',
        'সৌন্দয': 'সৌন্দর্য',
        'পদমযাদা': 'পদমর্যাদা',
        'মিিত': 'মিশ্রিত',
        'দ্ব্যথবোধক': 'দ্ব্যর্থবোধক',
        'দ্ব্যথ': 'দ্ব্যর্থ',
        'িমুখী': 'দ্বিমুখী',
        'িধাদ্বন্দ্ব': 'দ্বিধাদ্বন্দ্ব',
        'িধাগ্রস্ততা': 'দ্বিধাগ্রস্ততা',
        'বৎসনা': 'ভর্ৎসনা',
        'ভৎসনা': 'ভর্ৎসনা',
        'পরিবতনশীল': 'পরিবর্তনশীল',
        'পরিবতন': 'পরিবর্তন',
        'মিথ্যাা': 'মিথ্যা',
        'সন্ন্যাাসী': 'সন্ন্যাসী',
        'খাদ্যাাভ্যাাস': 'খাদ্যাভ্যাস',
        'সমাজকল্যাাণমূলক': 'সমাজকল্যাণমূলক',
        'কল্যাাণকর': 'কল্যাণকর',
        'বন্যাার': 'বন্যার',
        'অভ্যুত্থাান': 'অভ্যুত্থান',
        'পরিসংখ্যাান': 'পরিসংখ্যান',
        'স্টাার্টআপগুলো': 'স্টার্টআপগুলো',
        'অর্কেস্ট্রাা': 'অর্কেস্ট্রা',
        'উপন্যাাসের': 'উপন্যাসের',
        'অধ্যাায়টি': 'অধ্যায়টি',
        'অধ্যাাপক': 'অধ্যাপক',
        'প্রতিবর্ত ক্রি য়াকে': 'প্রতিবর্ত ক্রিয়াকে',
        'ক্রি য়া': 'ক্রিয়া',
        'স্নাায়ু': 'স্নায়ু',
        'ব্যাাহত': 'ব্যাহত',
        'নিখোঁঁজ': 'নিখোঁজ',
        'মুদ্রাস্ফীীতি': 'মুদ্রাস্ফীতি',
        'স্ফীীত': 'স্ফীত',
        'ক্ষণস্থায়ীী': 'ক্ষণস্থায়ী',
        'খ্যাাতি': 'খ্যাতি',
        'যোগব্যাায়াম': 'যোগব্যায়াম',
        'উস্কাানি': 'উস্কানি',
        'ক্যাাম্পাসের': 'ক্যাম্পাসের',
        'দুবল': 'দুর্বল',
        'মিটিংংয়ে': 'মিটিংয়ে',
        'আবেগপূণ': 'আবেগপূর্ণ',
        'কমকত্তা': 'কর্মকর্তা',
        'ধম': 'ধর্ম',
        'আকষণীয়': 'আকর্ষণীয়',
        'অধ্যাবসায়ী': 'অধ্যবসায়ী',
        'সতকতা': 'সতর্কতা',
        'অপবিত': 'অপবিত্র',
        'কমক্ষমতা': 'কর্মক্ষমতা',
        'কমী': 'কর্মী',
        'নিমজ্জি ত': 'নিমজ্জিত',
        'ক্ষো ভ': 'ক্ষোভ',
        'স্বয়ংক্রি য়': 'স্বয়ংক্রিয়',
        'শোনাচ্ছি ল': 'শোনাচ্ছিল',
        'হচ্ছি ল': 'হচ্ছিল',
        'কম্পি উটার': 'কম্পিউটার',
        'স্প্রে ডশিটটি': 'স্প্রেডশিটটি',
        'অনুচক্রি কা': 'অনুচক্রিকা',
        'বিচ্ছি ন্নতা': 'বিচ্ছিন্নতা',
        'উন্মো চনে': 'উন্মোচনে',
        'আকাঙ্ক্ষাা': 'আকাঙ্ক্ষা',
        'বহিস্কাার': 'বহিষ্কার'
    }
    for old, new in replacements.items():
        t = t.replace(old, new)
        
    t = re.sub(r'([\u09BE-\u09CC\u0981-\u0983])\1+', r'\1', t)
    return t

SPECIFIC_EXAMPLE_FIXES = {
    9: { # Aggregate (verb)
        2: {
            'en': 'The software will aggregate data from multiple servers into a single report.',
            'bn': 'সফটওয়্যারটি একাধিক সার্ভার থেকে তথ্য সংগ্রহ করে একটি একক প্রতিবেদনে একত্রিত করবে।'
        }
    },
    50: { # Coagulate (verb)
        1: {
            'en': 'Platelets in the blood help a wound coagulate quickly.',
            'bn': 'রক্তের অনুচক্রিকা ক্ষতের রক্ত দ্রুত জমাট বাঁধতে সাহায্য করে।'
        }
    },
    70: { # Default (noun)
        1: {
            'en': 'A sudden default on the commercial mortgage forced the bank to foreclose.',
            'bn': 'বাণিজ্যিক বন্ধকী ঋণের আকস্মিক খেলাপির কারণে ব্যাংক সম্পত্তি বাজেয়াপ্ত করতে বাধ্য হয়েছিল।'
        }
    },
    82: { # Diffuse (adjective)
        1: {
            'en': 'The photographer used a diffuse light to soften facial shadows.',
            'bn': 'আলোকচিত্রী মুখের ছায়াগুলো কোমল করতে একটি বিচ্ছুরিত আলো ব্যবহার করেছিলেন।'
        }
    },
    108: { # Dupe (verb)
        2: {
            'en': 'Phishing emails attempt to dupe unsuspecting users into revealing their passwords.',
            'bn': 'ফিশিং ইমেইলগুলো অসতর্ক ব্যবহারকারীদের বোকা বানিয়ে তাদের পাসওয়ার্ড হাতিয়ে নেওয়ার চেষ্টা করে।'
        }
    },
    141: { # Fledgling (noun)
        2: {
            'en': 'As a fledgling in the investment industry, she relied heavily on her senior mentor.',
            'bn': 'বিনিয়োগ শিল্পে একজন নবীন ব্যক্তি হিসেবে তিনি তার অভিজ্ঞ পরামর্শদাতার ওপর ব্যাপকভাবে নির্ভর করেছিলেন।'
        }
    },
    155: { # Harangue (noun)
        1: {
            'en': 'The senator delivered a furious harangue against the proposed spending cuts.',
            'bn': 'সিনেটর প্রস্তাবিত ব্যয় সংকোচনের বিরুদ্ধে এক তীব্র ও আক্রমণাত্মক ভাষণ দিয়েছিলেন।'
        }
    }
}

def main():
    print("Reading src/data/gre333.json...")
    with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Build candidate corpus by POS for distractor selection
    corpus_by_pos = {'verb': [], 'noun': [], 'adjective': [], 'adverb': []}
    for idx in range(1, 201):
        pos = CURATED_DATA[idx][0]
        word = data[idx - 1]['word']
        if word not in corpus_by_pos[pos]:
            corpus_by_pos[pos].append(word)

    # Update words 1 to 200
    for idx in range(1, 201):
        item = data[idx - 1]
        c = CURATED_DATA[idx]
        
        pos = c[0]
        pron_en = c[1]
        pron_bn = c[2]
        meaning_en = c[3]
        meaning_bn = c[4]
        syns = c[5]
        ants = c[6]
        
        # Clean examples
        ex1 = item['examples'][0]
        ex2 = item['examples'][1]
        
        clean_ex1 = {
            'en': ex1['en'].strip(),
            'bn': clean_bangla(ex1['bn'].strip())
        }
        clean_ex2 = {
            'en': ex2['en'].strip(),
            'bn': clean_bangla(ex2['bn'].strip())
        }
        
        if idx in SPECIFIC_EXAMPLE_FIXES:
            fixes = SPECIFIC_EXAMPLE_FIXES[idx]
            if 1 in fixes:
                clean_ex1 = fixes[1]
            if 2 in fixes:
                clean_ex2 = fixes[2]
        
        # Build 501 sentence completion question
        # Target word + 4 same-POS distractors
        cand_list = [cw for cw in corpus_by_pos[pos] if cw.lower() != item['word'].lower()]
        import random
        random.seed(idx * 73 + 17)
        distractors = random.sample(cand_list, min(4, len(cand_list)))
        while len(distractors) < 4:
            distractors.append(f"Alt-{len(distractors)}")
            
        opts = distractors + [item['word']]
        random.shuffle(opts)
        correct_idx = opts.index(item['word'])
        
        # Blank sentence from ex1
        pattern = re.compile(re.escape(item['word']), re.IGNORECASE)
        blanked = pattern.sub('_____', clean_ex1['en'])
        if '_____' not in blanked:
            blanked = f"The situation required someone who could _____ the requirements effectively."
            
        opt_meanings = []
        for opt in opts:
            if opt.lower() == item['word'].lower():
                opt_meanings.append(meaning_bn)
            else:
                # Find matching word meaning
                found = False
                for m_idx in range(1, 201):
                    if data[m_idx - 1]['word'].lower() == opt.lower():
                        opt_meanings.append(CURATED_DATA[m_idx][4])
                        found = True
                        break
                if not found:
                    opt_meanings.append("বিকল্প অর্থ")
                    
        sc = {
            "sentenceWithBlank": blanked,
            "options": opts,
            "correctIndex": correct_idx,
            "optionMeaningsBn": opt_meanings,
            "explanationEn": f"{item['word']} ({pos}.) means {meaning_en}",
            "sentenceTranslationBn": clean_ex1['bn']
        }
        
        # Update entry
        item['partOfSpeech'] = pos
        item['pronunciationEn'] = pron_en
        item['pronunciationBn'] = pron_bn
        item['meaningEn'] = meaning_en
        item['meaningBn'] = meaning_bn
        item['synonyms'] = syns
        item['antonyms'] = ants
        item['examples'] = [clean_ex1, clean_ex2]
        item['sentenceCompletion'] = sc

    print("Writing updated data back to src/data/gre333.json...")
    with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully updated all 200 words across Sets 1 to 10 in src/data/gre333.json!")

if __name__ == '__main__':
    main()
