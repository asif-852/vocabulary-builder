# -*- coding: utf-8 -*-
"""
Upgrades definitions and cleans data for GRE 333 Sets 11 to 17 (Words 201 to 333).
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

enhanced_definitions = {
    202: "Tending to talk a great deal; talkative and garrulous.",
    204: "Emitting or reflecting light; glowing, bright, or radiant.",
    207: "Capable of being shaped or bent; easily influenced, pliable, or adaptable.",
    209: "Characterized by lying or untruthfulness; dishonest or deceitful.",
    211: "Showing great attention to detail; very careful, precise, and scrupulous.",
    215: "Sullen, gloomy, and ill-tempered; sullenly melancholy.",
    216: "Lacking interest or excitement; dull, ordinary, and commonplace.",
    219: "Stubbornly refusing to change one's opinion or course of action; unyielding.",
    220: "Obedient or attentive to an excessive or servile degree; fawning.",
    223: "Assertive of authority in an annoying and domineering way; meddlesome.",
    224: "Involving great effort, burden, or difficulty; burdensome and oppressive.",
    225: "Harsh criticism or censure; disgrace arising from shameful conduct.",
    227: "Characterized by vulgar or pretentious display; designed to impress.",
    230: "Involving or caused by a physical or mental disease; compulsive or abnormal.",
    233: "A strong or habitual liking for something; a marked inclination or bias.",
    236: "Deceitful and untrustworthy; treacherous and disloyal.",
    237: "Carried out with minimal effort, care, or interest; hasty and routine.",
    239: "Spreading widely throughout an area or group of people; all-encompassing.",
    240: "Having an unemotional and stolidly calm disposition; placid and composed.",
    243: "The quality of being easily shaped, molded, or adapted without breaking.",
    244: "A remark or statement, especially one with moral content, that is trite or cliché.",
    245: "A large or excessive amount of something; an overabundance.",
    247: "Having minute spaces or holes through which liquid or air may pass; permeable.",
    250: "Not securely held or in position; dangerously insecure, uncertain, or risky.",
    253: "Failing to observe the limits of what is permitted or appropriate; audaciously bold.",
    257: "Constituting or presenting a problem; doubtful, uncertain, or questionable.",
    260: "Serving to forbid or restrict; excessively high or difficult to afford.",
    262: "An innate inclination or natural tendency to behave in a particular way.",
    264: "The state or quality of conforming to accepted standards of good behavior and decorum.",
    266: "Having a sharp and caustic quality; biting, acrid, or cutting in expression.",
    267: "Limited, restricted, or conditional rather than absolute; partial.",
    269: "In a state or period of dormancy, rest, or temporary inactivity.",
    270: "Elevated, lofty, or esoteric in character; of thin density (of atmosphere).",
    273: "A person who lives a solitary life and tends to avoid other people; a hermit.",
    274: "Difficult to understand, abstruse, obscure, or little-known.",
    279: "An unprincipled, wicked, or shameless person; devoid of moral scruples.",
    288: "To give official permission or approval for; also to impose a penalty on.",
    294: "A person inclined to question or doubt all accepted opinions or claims.",
    295: "Characterized by or showing interest, care, or attentive concern.",
    296: "Tending to induce drowsiness or sleep; sleep-inducing.",
    297: "Superficially plausible, but actually wrong, deceptive, or misleading.",
    303: "Calm, dependable, and showing little emotion or animation; phlegmatic.",
    304: "Marked with thin, parallel stripes, grooves, or bands.",
    307: "A formal legal writ compelling a witness to attend and testify in court.",
    311: "An uncertain belief, assumption, or hypothesis based on incomplete evidence.",
    312: "Understood or implied without being stated directly; unspoken.",
    313: "Diverging from a central topic; merely touching upon something superficially.",
    314: "Very weak, slender, slight, or insubstantial; tenuous grasp.",
    315: "A long, angry speech of criticism, accusation, or violent denunciation.",
    323: "Habitually speaking the truth; strictly truthful and honest.",
    324: "Using or expressed in more words than are needed; wordy and verbose.",
    326: "Having a thick, sticky consistency between solid and liquid; high viscosity.",
    327: "Bitter, abusive, and harshly critical in tone; disparaging.",
    331: "A confused, tangled mass or jumble; a state of general turmoil."
}

updated = 0
for idx, defn in enhanced_definitions.items():
    corpus[idx - 1]['meaningEn'] = defn
    updated += 1

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"Successfully applied {updated} enhanced GRE definitions to Sets 11 to 17!")
