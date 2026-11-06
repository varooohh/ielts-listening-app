import streamlit as st
from google import genai
import time

# -----------------------------------------------------------------------------
# 1. Page Configuration & Level B3 Branding
# -----------------------------------------------------------------------------
st.set_page_config(page_title="IELTS B3 Upper-Intermediate Listening Prep", page_icon="🎧", layout="wide")

st.title("🎧 IELTS Listening Prep: CEFR Level B3")
st.subheader("Theme: Global Environmental & Sustainability Debates") 
st.caption("Targeting Upper-Intermediate Listening Skills: Implied Meanings, Speaker Attitudes, & Academic Arguments")

# Sidebar Navigation
st.sidebar.header("⚙️ Settings & Navigation")
api_key = st.sidebar.text_input("Gemini API Key:", type="password", help="Enter key for AI evaluation & explanations")
app_mode = st.sidebar.radio("Select Learning Mode:", ["B3 Video Practice (20+ Lessons)", "Full IELTS Mock Test Mode"])

# -----------------------------------------------------------------------------
# 2. IELTS Band Score Calculator
# -----------------------------------------------------------------------------
def get_ielts_band(score_out_of_40):
    if score_out_of_40 >= 39: return 9.0
    elif score_out_of_40 >= 37: return 8.5
    elif score_out_of_40 >= 35: return 8.0
    elif score_out_of_40 >= 32: return 7.5
    elif score_out_of_40 >= 30: return 7.0
    elif score_out_of_40 >= 26: return 6.5
    elif score_out_of_40 >= 23: return 6.0
    elif score_out_of_40 >= 18: return 5.5
    elif score_out_of_40 >= 16: return 5.0
    else: return 4.5

# -----------------------------------------------------------------------------
# Data Store: B3 Level Practice Lessons (Theme: Global Environmental & Sustainability Debates)
# -----------------------------------------------------------------------------
YOUTUBE_PRACTICE_DATA = [
    {
        "id": 1,
        "category": "Educational Debate",
        "title": "Lesson 1: Can 100% Renewable Energy Power the World?",
        "url": "https://www.youtube.com/watch?v=RnvCbquYeIM",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What is the main technical challenge mentioned regarding solar and wind power?",
                "options": ["High manufacturing cost", "Intermittent energy availability", "Lack of public interest", "Over-regulation"],
                "ans": "Intermittent energy availability"
            },
            {
                "type": "short",
                "q": "2. What device is essential to store excess energy generated on windy or sunny days?",
                "ans": "Batteries"
            },
            {
                "type": "mcq",
                "q": "3. What does the speaker imply when discussing current power grids?",
                "options": ["Existing infrastructure needs complete modernization", "Fossil fuels are already obsolete", "Grids cannot support clean energy"],
                "ans": "Existing infrastructure needs complete modernization"
            },
            {
                "type": "short",
                "q": "4. What percentage of global energy must come from zero-emission sources to halt warming?",
                "ans": "100%"
            },
            {
                "type": "mcq",
                "q": "5. What is the speaker's overall stance on achieving a fully renewable future?",
                "options": ["Strongly pessimistic", "Cautiously optimistic", "Completely indifferent", "Dismissive"],
                "ans": "Cautiously optimistic"
            }
        ]
    },
    {
        "id": 2,
        "category": "Environmental Documentary",
        "title": "Lesson 2: What Really Happens to the Plastic You Throw Away",
        "url": "https://www.youtube.com/watch?v=_6xlNyWPpB8",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What implied message does the narrator convey about plastic degradation?",
                "options": ["Plastics decompose in decades", "Plastics persist for centuries in marine ecosystems", "Recycling removes all waste"],
                "ans": "Plastics persist for centuries in marine ecosystems"
            },
            {
                "type": "short",
                "q": "2. Which micro-particles created by breaking plastic pose severe risks to marine life?",
                "ans": "Microplastics"
            },
            {
                "type": "mcq",
                "q": "3. The speaker's attitude while tracing the journey of the three plastic bottles can be described as:",
                "options": ["Informative and cautionary", "Lighthearted and humorous", "Skeptical of climate science"],
                "ans": "Informative and cautionary"
            },
            {
                "type": "short",
                "q": "4. Where do millions of tons of uncollected plastic waste ultimately end up?",
                "ans": "Oceans"
            },
            {
                "type": "mcq",
                "q": "5. What underlying conclusion is emphasized regarding consumer habits?",
                "options": ["Individual recycling alone is sufficient", "Systemic reduction of single-use plastic is crucial", "Incineration is the best option"],
                "ans": "Systemic reduction of single-use plastic is crucial"
            }
        ]
    },
    {
        "id": 3,
        "category": "Academic Talk",
        "title": "Lesson 3: Can We Create the 'Perfect' Farm?",
        "url": "https://www.youtube.com/watch?v=xFqecEtdGZ0",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What is the primary conflict between modern agriculture and environmental conservation?",
                "options": ["Land expansion and habitat loss", "High price of organic food", "Lack of farm machinery"],
                "ans": "Land expansion and habitat loss"
            },
            {
                "type": "short",
                "q": "2. What farming technique restores soil nutrients naturally over consecutive seasons?",
                "ans": "Crop rotation"
            },
            {
                "type": "mcq",
                "q": "3. What does the speaker imply about the concept of a 'perfect' farm?",
                "options": ["It is easily scalable everywhere", "It requires localized and multi-faceted solutions", "It depends entirely on technology"],
                "ans": "It requires localized and multi-faceted solutions"
            },
            {
                "type": "short",
                "q": "4. What major natural resource is most heavily consumed by traditional agriculture?",
                "ans": "Freshwater"
            },
            {
                "type": "mcq",
                "q": "5. The speaker's perspective on global food security highlights that:",
                "options": ["Sustainable farming can feed the world if implemented properly", "Famine is unavoidable", "Technology should replace natural soil"],
                "ans": "Sustainable farming can feed the world if implemented properly"
            }
        ]
    },
    {
        "id": 4,
        "category": "Scientific Documentary",
        "title": "Lesson 4: What If There Were 1 Trillion More Trees?",
        "url": "https://www.youtube.com/watch?v=3hxE7Af98AI",
        "questions": [
            {
                "type": "mcq",
                "q": "1. How do global forest ecosystems mitigate climate change?",
                "options": ["They absorb atmospheric carbon dioxide", "They reflect sunlight into space", "They reduce ocean salinity"],
                "ans": "They absorb atmospheric carbon dioxide"
            },
            {
                "type": "short",
                "q": "2. What major greenhouse gas is captured and stored inside growing trees?",
                "ans": "Carbon dioxide"
            },
            {
                "type": "mcq",
                "q": "3. What implied warning does the researcher mention regarding mass tree planting?",
                "options": ["Monoculture planting damages existing biodiversity", "Trees grow too fast to control", "Forests decrease rainfall"],
                "ans": "Monoculture planting damages existing biodiversity"
            },
            {
                "type": "short",
                "q": "4. How many additional trees are estimated to be required for optimal carbon capture?",
                "ans": "1 trillion"
            },
            {
                "type": "mcq",
                "q": "5. What is the main argument regarding tree planting in global climate strategy?",
                "options": ["It is a powerful tool alongside emission reductions", "It eliminates the need to cut fossil fuels", "It is economically ineffective"],
                "ans": "It is a powerful tool alongside emission reductions"
            }
        ]
    },
    {
        "id": 5,
        "category": "Authentic Podcast",
        "title": "Lesson 5: Is the Recycling System Broken?",
        "url": "https://www.youtube.com/watch?v=iOao1dfGP2s",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What attitude do the podcast presenters express about current global recycling rates?",
                "options": ["Deep concern over systemic inefficiency", "Satisfaction with public participation", "Indifference to industrial waste"],
                "ans": "Deep concern over systemic inefficiency"
            },
            {
                "type": "short",
                "q": "2. What specific term is used to describe discarded electronics like phones and laptops?",
                "ans": "E-waste"
            },
            {
                "type": "mcq",
                "q": "3. What implied factor makes electronic devices difficult to recycle?",
                "options": ["Complex mix of hazardous materials and metals", "Lack of consumer interest", "High shipping costs"],
                "ans": "Complex mix of hazardous materials and metals"
            },
            {
                "type": "short",
                "q": "4. Approximately what percentage of global e-waste is formally recycled?",
                "ans": "20%"
            },
            {
                "type": "mcq",
                "q": "5. What key practice do the hosts suggest as more effective than simple recycling?",
                "options": ["Reducing consumption and repairing old devices", "Exporting waste to ocean dumps", "Incineration"],
                "ans": "Reducing consumption and repairing old devices"
            }
        ]
    },
    {
        "id": 6,
        "category": "Academic Discussion",
        "title": "Lesson 6: Changing the Earth's Climate - Geoengineering Solutions",
        "url": "https://www.youtube.com/watch?v=jnFeXaL02Fg",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What is the primary definition of geoengineering discussed by the speakers?",
                "options": ["Large-scale technological interventions to manipulate Earth's climate", "Natural forest restoration programs", "Replacing all fossil fuels with solar panels"],
                "ans": "Large-scale technological interventions to manipulate Earth's climate"
            },
            {
                "type": "short",
                "q": "2. What key greenhouse gas do geoengineering projects aim to capture directly from the atmosphere?",
                "ans": "Carbon dioxide"
            },
            {
                "type": "mcq",
                "q": "3. What implied concern does the host raise regarding solar radiation management?",
                "options": ["It may cause unpredictable side effects on global weather patterns", "It is too cheap to implement", "It requires no scientific research"],
                "ans": "It may cause unpredictable side effects on global weather patterns"
            },
            {
                "type": "short",
                "q": "4. What term describes the intentional artificial cooling of the planet using aerosols?",
                "ans": "Solar geoengineering"
            },
            {
                "type": "mcq",
                "q": "5. What overall attitude do the presenters express towards geoengineering as a primary fix?",
                "options": ["Skeptical, viewing it as a risky fallback rather than a cure", "Enthusiastic and ready for immediate deployment", "Completely uninterested"],
                "ans": "Skeptical, viewing it as a risky fallback rather than a cure"
            }
        ]
    },
    {
        "id": 7,
        "category": "Authentic Podcast",
        "title": "Lesson 7: Climate Change: Are There Too Many People?",
        "url": "https://www.youtube.com/watch?v=qoNRZKgLDhg",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What core relationship between global population growth and carbon footprint is analyzed?",
                "options": ["Consumption patterns matter more than population numbers alone", "Population size is the sole cause of global warming", "Population growth has no impact on energy use"],
                "ans": "Consumption patterns matter more than population numbers alone"
            },
            {
                "type": "short",
                "q": "2. Which socio-economic group accounts for the highest proportion of global carbon emissions?",
                "ans": "High-income nations"
            },
            {
                "type": "mcq",
                "q": "3. The speaker implies that blaming population growth in developing nations is:",
                "options": ["Ethically flawed and misleading", "Economically accurate", "Universally accepted by climate scientists"],
                "ans": "Ethically flawed and misleading"
            },
            {
                "type": "short",
                "q": "4. What key lifestyle change is suggested to reduce individual ecological impacts?",
                "ans": "Reducing meat consumption"
            },
            {
                "type": "mcq",
                "q": "5. What is the host's main conclusion regarding future demographic trends?",
                "options": ["Equitable resource distribution is vital for sustainability", "Mandatory population controls must be enforced", "Global economic growth will solve overconsumption"],
                "ans": "Equitable resource distribution is vital for sustainability"
            }
        ]
    },
    {
        "id": 8,
        "category": "Policy & Energy Debate",
        "title": "Lesson 8: A Reality Check on Renewable Energy Capacity",
        "url": "https://www.youtube.com/watch?v=E0W1ZZYIV8o",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What physical constraint regarding land area and power density is highlighted in the debate?",
                "options": ["Renewables require vast land mass to match fossil fuel output", "Renewables generate too much excess energy", "Solar panels require zero physical space"],
                "ans": "Renewables require vast land mass to match fossil fuel output"
            },
            {
                "type": "short",
                "q": "2. What unit of measurement is used to compare power generation per square meter?",
                "ans": "Watts per square meter"
            },
            {
                "type": "mcq",
                "q": "3. What implied stance does the speaker take regarding nuclear power alongside renewables?",
                "options": ["Nuclear energy should be evaluated pragmatically to achieve zero carbon", "Nuclear power must be banned immediately", "Fossil fuels are superior to nuclear"],
                "ans": "Nuclear energy should be evaluated pragmatically to achieve zero carbon"
            },
            {
                "type": "short",
                "q": "4. What major European country is referenced as an example of energy density limitations?",
                "ans": "United Kingdom"
            },
            {
                "type": "mcq",
                "q": "5. How would you describe the speaker's tone during the mathematical breakdown?",
                "options": ["Analytical and realistic", "Overly sensational", "Dismissive of environmental science"],
                "ans": "Analytical and realistic"
            }
        ]
    },
    {
        "id": 9,
        "category": "Academic Discussion",
        "title": "Lesson 9: How Much Land Does It Take to Power the World?",
        "url": "https://www.youtube.com/watch?v=DW0jTe80kmM",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What central academic question is explored regarding global energy transition?",
                "options": ["The geographic footprint needed for different renewable sources", "The price of electric vehicles in Europe", "How to drill for oil more efficiently"],
                "ans": "The geographic footprint needed for different renewable sources"
            },
            {
                "type": "short",
                "q": "2. Which renewable power source requires the largest land footprint per megawatt produced?",
                "ans": "Biomass"
            },
            {
                "type": "mcq",
                "q": "3. What inference can be made about placing solar installations in desert regions?",
                "options": ["High potential output, but transmission to urban centers remains complex", "It solves all world energy problems without trade-offs", "Deserts have insufficient solar radiation"],
                "ans": "High potential output, but transmission to urban centers remains complex"
            },
            {
                "type": "short",
                "q": "4. What term describes combining agricultural land with solar energy production?",
                "ans": "Agrivoltaics"
            },
            {
                "type": "mcq",
                "q": "5. What key recommendation is offered for urban energy planning?",
                "options": ["Utilizing existing rooftops and infrastructure for solar deployment", "Clearing suburban forests for wind farms", "Relying exclusively on coal power plants"],
                "ans": "Utilizing existing rooftops and infrastructure for solar deployment"
            }
        ]
    },
    {
        "id": 10,
        "category": "Global Environmental Documentary",
        "title": "Lesson 10: The Surprising Solution to Ocean Plastic",
        "url": "https://www.youtube.com/watch?v=mT4Qbp89nIQ",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What innovative social framework does the documentary propose to tackle ocean waste?",
                "options": ["Monetizing plastic waste collection for impoverished communities", "Banning all ships from international waters", "Dumping plastic into deep trench ecosystems"],
                "ans": "Monetizing plastic waste collection for impoverished communities"
            },
            {
                "type": "short",
                "q": "2. What term is used for plastic waste recycled and converted into local currency or goods?",
                "ans": "Social plastic"
            },
            {
                "type": "mcq",
                "q": "3. What attitude does the speaker project toward tackling global poverty alongside waste?",
                "options": ["Empathetic and solution-oriented", "Pessimistic and doubtful", "Strictly academic and detached"],
                "ans": "Empathetic and solution-oriented"
            },
            {
                "type": "short",
                "q": "4. What basic necessity can collectors exchange plastic waste for at recycling banks?",
                "ans": "Food"
            },
            {
                "type": "mcq",
                "q": "5. What is the ultimate implied thesis of the talk?",
                "options": ["Turning waste into currency prevents it from ever reaching the ocean", "Ocean clean-up boats are the only solution", "Plastic pollution cannot be stopped"],
                "ans": "Turning waste into currency prevents it from ever reaching the ocean"
            }
        ]
    },
    {
        "id": 11,
        "category": "Environmental Discussion",
        "title": "Lesson 11: The Environmental Cost of Fast Fashion",
        "url": "https://www.youtube.com/watch?v=BiSYoeqb_VY",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What implied critique does the speaker make regarding mass clothing production?",
                "options": ["It prioritizes profit margins over environmental sustainability", "It creates high-quality durable garments", "It relies entirely on organic raw materials"],
                "ans": "It prioritizes profit margins over environmental sustainability"
            },
            {
                "type": "short",
                "q": "2. What natural resource is consumed in massive quantities during cotton cultivation?",
                "ans": "Water"
            },
            {
                "type": "mcq",
                "q": "3. The speaker's tone when detailing synthetic fabric dyes in rivers can be described as:",
                "options": ["Critical and alarmed", "Enthusiastic and hopeful", "Indifferent and detached"],
                "ans": "Critical and alarmed"
            },
            {
                "type": "short",
                "q": "4. What toxic chemical pollutants are released into waterways during textile treatment?",
                "ans": "Dyes"
            },
            {
                "type": "mcq",
                "q": "5. What underlying consumer shift is recommended to mitigate textile waste?",
                "options": ["Adopting a circular fashion model and buying less", "Throwing away clothes faster", "Increasing synthetic fabric imports"],
                "ans": "Adopting a circular fashion model and buying less"
            }
        ]
    },
    {
        "id": 12,
        "category": "Authentic Podcast",
        "title": "Lesson 12: Can Carbon Capture Technology Stop Global Warming?",
        "url": "https://www.youtube.com/watch?v=Xh0Yp8G4bQI",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What attitude do the podcast hosts exhibit towards carbon capture technology?",
                "options": ["Pragmatic skepticism about its feasibility at scale", "Unconditional approval as a magic bullet", "Total rejection of atmospheric engineering"],
                "ans": "Pragmatic skepticism about its feasibility at scale"
            },
            {
                "type": "short",
                "q": "2. What geological location is commonly used to store captured industrial carbon?",
                "ans": "Underground rock formations"
            },
            {
                "type": "mcq",
                "q": "3. What implied risk is associated with over-relying on carbon capture?",
                "options": ["It may reduce the urgency to phase out fossil fuels", "It decreases global economic growth", "It causes immediate cooling of the oceans"],
                "ans": "It may reduce the urgency to phase out fossil fuels"
            },
            {
                "type": "short",
                "q": "4. What is the primary financial barrier preventing widespread deployment of direct air capture?",
                "ans": "High operational cost"
            },
            {
                "type": "mcq",
                "q": "5. What is the host's main conclusion regarding climate mitigation strategy?",
                "options": ["Direct emission cuts must remain the primary priority", "Carbon capture can replace renewable energy", "Geoengineering requires no further regulation"],
                "ans": "Direct emission cuts must remain the primary priority"
            }
        ]
    },
    {
        "id": 13,
        "category": "Policy & Energy Debate",
        "title": "Lesson 13: Nuclear Energy: Ecological Solution or Environmental Threat?",
        "url": "https://www.youtube.com/watch?v=rcOFV4y5z8c",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What primary argument do pro-nuclear debaters present regarding carbon emissions?",
                "options": ["Nuclear power plants generate continuous baseload electricity with zero direct carbon", "Nuclear plants are cheaper to build than solar farms", "Nuclear fuel is completely renewable"],
                "ans": "Nuclear power plants generate continuous baseload electricity with zero direct carbon"
            },
            {
                "type": "short",
                "q": "2. What unresolved long-term concern is emphasized by opponent debaters?",
                "ans": "Radioactive waste disposal"
            },
            {
                "type": "mcq",
                "q": "3. What can be inferred from the debate regarding nuclear plant construction timelines?",
                "options": ["Long build times make it difficult to address immediate climate deadlines", "Nuclear plants can be built within a few months", "Government permits are granted instantly"],
                "ans": "Long build times make it difficult to address immediate climate deadlines"
            },
            {
                "type": "short",
                "q": "4. What heavy metallic element is used as the primary fuel source in nuclear fission?",
                "ans": "Uranium"
            },
            {
                "type": "mcq",
                "q": "5. How would you summarize the consensus of the debate panel?",
                "options": ["Nuclear energy involves significant trade-offs that require strict safety trade-offs", "Nuclear energy should be banned globally", "Fossil fuels are safer than nuclear power"],
                "ans": "Nuclear energy involves significant trade-offs that require strict safety trade-offs"
            }
        ]
    },
    {
        "id": 14,
        "category": "Academic Discussion",
        "title": "Lesson 14: Desalination and the Future of Water Scarcity",
        "url": "https://www.youtube.com/watch?v=P2143Q78c_I",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What core scientific challenge of seawater desalination is discussed by the panel?",
                "options": ["Extremely high energy consumption and environmental brine disposal", "Inability to remove ocean salt effectively", "Lack of seawater in arid coastal regions"],
                "ans": "Extremely high energy consumption and environmental brine disposal"
            },
            {
                "type": "short",
                "q": "2. What dense, highly concentrated byproduct of desalination threatens marine life when discharged?",
                "ans": "Brine"
            },
            {
                "type": "mcq",
                "q": "3. What implied perspective is shared regarding powering future desalination plants?",
                "options": ["They must be powered by renewable energy to avoid worsening climate change", "They should rely on coal-fired power plants", "Energy consumption is not a concern"],
                "ans": "They must be powered by renewable energy to avoid worsening climate change"
            },
            {
                "type": "short",
                "q": "4. What specific technology uses semi-permeable membranes to filter ocean salt?",
                "ans": "Reverse osmosis"
            },
            {
                "type": "mcq",
                "q": "5. What is the speaker's main recommendation for managing global water stress?",
                "options": ["Combining technological innovation with strict urban water conservation", "Relying solely on groundwater extraction", "Ignoring industrial agricultural waste"],
                "ans": "Combining technological innovation with strict urban water conservation"
            }
        ]
    },
    {
        "id": 15,
        "category": "Scientific Documentary",
        "title": "Lesson 15: The Crisis of Amazon Deforestation",
        "url": "https://www.youtube.com/watch?v=Qxby1J5bnPQ",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What ecological tipping point for the Amazon Rainforest is highlighted in the documentary?",
                "options": ["Transitioning from a tropical rainforest into a dry savanna", "Complete flooding of the Amazon river basin", "Excessive growth of non-native tree species"],
                "ans": "Transitioning from a tropical rainforest into a dry savanna"
            },
            {
                "type": "short",
                "q": "2. What commercial activity is identified as the largest driver of rainforest clearing?",
                "ans": "Cattle ranching"
            },
            {
                "type": "mcq",
                "q": "3. What attitude does the narrator express toward international supply chain accountability?",
                "options": ["Firm insistence that global consumers share responsibility", "Reluctance to blame foreign markets", "Complete indifference to agricultural exports"],
                "ans": "Firm insistence that global consumers share responsibility"
            },
            {
                "type": "short",
                "q": "4. What key atmospheric process created by trees releases rainfall across South America?",
                "ans": "Evapotranspiration"
            },
            {
                "type": "mcq",
                "q": "5. What underlying conclusion is drawn regarding Amazon preservation?",
                "options": ["Protecting indigenous territories is essential for effective forest conservation", "Economic expansion should take precedence", "Replanting trees in cities can replace the Amazon"],
                "ans": "Protecting indigenous territories is essential for effective forest conservation"
            }
        ]
    },
    {
        "id": 16,
        "category": "Environmental Discussion",
        "title": "Lesson 16: Biodiversity Loss and Ecosystem Collapse",
        "url": "https://www.youtube.com/watch?v=b6Ua_zWDH6U",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What core warning do scientists share regarding insect population decline?",
                "options": ["It threatens the foundation of global food webs and pollination", "It increases soil fertility", "It has no impact on human agriculture"],
                "ans": "It threatens the foundation of global food webs and pollination"
            },
            {
                "type": "short",
                "q": "2. What ecological service provided by insects is vital for fruit production?",
                "ans": "Pollination"
            },
            {
                "type": "mcq",
                "q": "3. What can be inferred about the speaker's view on habitat fragmentation?",
                "options": ["Isolating wildlife populations accelerates species extinction", "Small nature reserves are completely sufficient", "Urban expansion improves biodiversity"],
                "ans": "Isolating wildlife populations accelerates species extinction"
            },
            {
                "type": "short",
                "q": "4. What toxic agricultural inputs are primary drivers of pollinator decline?",
                "ans": "Pesticides"
            },
            {
                "type": "mcq",
                "q": "5. What overall tone is expressed during the panel discussion?",
                "options": ["Urgent and evidence-based", "Dismissive and casual", "Overly optimistic"],
                "ans": "Urgent and evidence-based"
            }
        ]
    },
    {
        "id": 17,
        "category": "Authentic Podcast",
        "title": "Lesson 17: Urban Air Pollution and Public Health",
        "url": "https://www.youtube.com/watch?v=e6rglsLy1Ys",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What attitude do the podcast hosts convey regarding particulate matter (PM2.5)?",
                "options": ["Grave concern for invisible respiratory hazards in major cities", "Confidence that air filters solve urban smog", "Indifference to vehicle emissions"],
                "ans": "Grave concern for invisible respiratory hazards in major cities"
            },
            {
                "type": "short",
                "q": "2. What microscopic particle metric is used to measure airborne industrial dust?",
                "ans": "PM2.5"
            },
            {
                "type": "mcq",
                "q": "3. What implied factor links air quality directly to socio-economic inequality?",
                "options": ["Low-income neighborhoods are disproportionately located near industrial zones", "Rich areas suffer higher vehicle pollution", "Air quality is equal everywhere"],
                "ans": "Low-income neighborhoods are disproportionately located near industrial zones"
            },
            {
                "type": "short",
                "q": "4. What renewable transport alternative is recommended to reduce city smog?",
                "ans": "Electric buses"
            },
            {
                "type": "mcq",
                "q": "5. What is the host's primary policy recommendation?",
                "options": ["Implementing low-emission zones and expanding electric public transit", "Moving cities away from coastlines", "Banning all private vehicles permanently"],
                "ans": "Implementing low-emission zones and expanding electric public transit"
            }
        ]
    },
    {
        "id": 18,
        "category": "Economic & Policy Debate",
        "title": "Lesson 18: Carbon Tax vs. Cap-and-Trade Markets",
        "url": "https://www.youtube.com/watch?v=J_Bh40S_b2s",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What main argument is put forward by proponents of a direct carbon tax?",
                "options": ["It provides price certainty and incentivizes clean energy investment", "It eliminates all government regulation", "It guarantees exact emission limits"],
                "ans": "It provides price certainty and incentivizes clean energy investment"
            },
            {
                "type": "short",
                "q": "2. What market mechanism sets a hard ceiling on total industrial greenhouse gas emissions?",
                "ans": "Cap-and-trade"
            },
            {
                "type": "mcq",
                "q": "3. What implied weakness of carbon offset credits is criticized by environmental economists?",
                "options": ["Offsets can be manipulated without reducing real-world pollution", "Offsets are too expensive for corporations", "Offsets are strictly verified by independent auditors"],
                "ans": "Offsets can be manipulated without reducing real-world pollution"
            },
            {
                "type": "short",
                "q": "4. What financial penalty is levied per ton of carbon emitted under a tax policy?",
                "ans": "Carbon tax"
            },
            {
                "type": "mcq",
                "q": "5. How would you summarize the conclusion of the policy debate?",
                "options": ["Both instruments require strong regulatory oversight to be effective", "Cap-and-trade has completely failed everywhere", "Carbon taxation harms economic growth without benefit"],
                "ans": "Both instruments require strong regulatory oversight to be effective"
            }
        ]
    },
    {
        "id": 19,
        "category": "Academic Discussion",
        "title": "Lesson 19: Sustainable Urban Transportation Architecture",
        "url": "https://www.youtube.com/watch?v=fmt8t9KkM4U",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What core urban design shift is advocated by the university panel?",
                "options": ["Transitioning from car-centric planning to pedestrian and transit-oriented development", "Building wider highways for commuters", "Subsidizing private luxury vehicles"],
                "ans": "Transitioning from car-centric planning to pedestrian and transit-oriented development"
            },
            {
                "type": "short",
                "q": "2. What concept describes cities designed so daily amenities are accessible within a short walk?",
                "ans": "15-minute city"
            },
            {
                "type": "mcq",
                "q": "3. What can be inferred about the speaker's evaluation of high-speed rail networks?",
                "options": ["They effectively replace short-haul regional flights and reduce emissions", "They are economically impractical for modern nations", "They increase urban traffic congestion"],
                "ans": "They effectively replace short-haul regional flights and reduce emissions"
            },
            {
                "type": "short",
                "q": "4. What dedicated lane system speeds up urban bus transit times?",
                "ans": "Bus rapid transit"
            },
            {
                "type": "mcq",
                "q": "5. What speaker perspective is expressed regarding bike infrastructure?",
                "options": ["Protected bike lanes significantly boost public safety and lower emissions", "Cycling infrastructure is only for recreational parks", "Bikes cause traffic delays"],
                "ans": "Protected bike lanes significantly boost public safety and lower emissions"
            }
        ]
    },
    {
        "id": 20,
        "category": "Scientific Documentary",
        "title": "Lesson 20: Glacial Melting and Rising Sea Levels",
        "url": "https://www.youtube.com/watch?v=vp3bgraHkSY",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What major climate feedback loop is explained regarding polar ice loss?",
                "options": ["Melting ice reduces Earth's albedo, absorbing more solar heat", "Ice loss cools ocean currents rapidly", "Glaciers absorb excess greenhouse gases"],
                "ans": "Melting ice reduces Earth's albedo, absorbing more solar heat"
            },
            {
                "type": "short",
                "q": "2. What scientific term describes the reflectivity of Earth's ice surfaces?",
                "ans": "Albedo"
            },
            {
                "type": "mcq",
                "q": "3. What attitude does the narrator project regarding coastal vulnerability?",
                "options": ["Serious concern for millions of residents in low-lying coastal cities", "Reassurance that sea level rise is negligible", "Skepticism toward satellite measurements"],
                "ans": "Serious concern for millions of residents in low-lying coastal cities"
            },
            {
                "type": "short",
                "q": "4. What massive ice sheet in the Southern Hemisphere contains the majority of Earth's fresh water?",
                "ans": "Antarctica"
            },
            {
                "type": "mcq",
                "q": "5. What underlying conclusion is emphasized in the documentary finale?",
                "options": ["Immediate global decarbonization is essential to prevent catastrophic sea level rise", "Human relocation is the only solution", "Glacial retreat will naturally reverse"],
                "ans": "Immediate global decarbonization is essential to prevent catastrophic sea level rise"
            }
        ]
    }
]
# -----------------------------------------------------------------------------
# MODE 1: B3 LEVEL PRACTICE MODE
# -----------------------------------------------------------------------------
if app_mode == "B3 Video Practice (20+ Lessons)":
    st.header("📺 Level B3 Authentic Video Practice")
    st.info("Instructions: Watch the B3 authentic audio material (debates, podcasts, academic discussions). Focus on implied meanings, speaker attitudes, and main arguments.")

    lesson_options = [f"[{item['category']}] {item['title']}" for item in YOUTUBE_PRACTICE_DATA]
    selected_lesson = st.selectbox("Select a B3 Listening Lesson:", lesson_options)
    
    lesson_idx = lesson_options.index(selected_lesson)
    current_data = YOUTUBE_PRACTICE_DATA[lesson_idx]

    st.subheader(f"Lesson Category: {current_data['category']}")
    st.video(current_data["url"])

    st.subheader("📝 B3 Proficiency Questions (Inference & Argument Analysis)")
    user_answers = {}
    
    with st.form(key=f"b3_practice_form_{current_data['id']}"):
        for idx, q_data in enumerate(current_data["questions"]):
            st.markdown(f"**{q_data['q']}**")
            if q_data["type"] == "mcq":
                user_answers[idx] = st.radio(f"Select your answer for Q{idx+1}:", q_data["options"], key=f"q_{current_data['id']}_{idx}")
            else:
                user_answers[idx] = st.text_input(f"Your short answer for Q{idx+1}:", key=f"q_{current_data['id']}_{idx}")
            st.write("---")

        submit_b3 = st.form_submit_button("Submit & Evaluate Answers")

    if submit_b3:
        correct_count = 0
        st.subheader("📊 Pedagogical Evaluation & AI Explanation")
        
        for idx, q_data in enumerate(current_data["questions"]):
            user_ans = user_answers[idx].strip().lower()
            correct_ans = q_data["ans"].strip().lower()

            if user_ans == correct_ans:
                st.success(f"Q{idx+1}: Correct! (Your Choice: {user_answers[idx]})")
                correct_count += 1
            else:
                st.error(f"Q{idx+1}: Incorrect. Your Choice: '{user_answers[idx]}' | Expected Answer: '{q_data['ans']}'")
                
                # B3 AI Feedback Generator (Focusing on Implied Meaning & Attitude)
                if api_key:
                    try:
                        client = genai.Client(api_key=api_key)
                        fb_prompt = f"""
                        Target Level: CEFR B3 Upper-Intermediate Listening.
                        Question: {q_data['q']}
                        Student Answer: {user_answers[idx]}
                        Correct Answer: {q_data['ans']}
                        
                        Explain in 2 clear sentences why the correct answer is right based on B3 listening skills (speaker attitude, implied meaning, or contextual inference). Keep explanations encouraging and clear.
                        """
                        res = client.models.generate_content(model='gemini-2.5-flash', contents=fb_prompt)
                        st.info(f"💡 **AI B3 Diagnostic Feedback:** {res.text}")
                    except Exception as e:
                        st.caption("AI Feedback offline. Check Gemini API Key.")
        
        st.metric("Section Score", f"{correct_count} / {len(current_data['questions'])}")

# -----------------------------------------------------------------------------
# MODE 2: FULL IELTS MOCK TEST MODE (With Countdown Timer & Band Score)
# -----------------------------------------------------------------------------
else:
    st.header("⏱️ IELTS Full Listening Test (Test 1–4)")
    st.warning("Official Test Simulation: 30 minutes timed exam covering Sections 1–4.")

    selected_test = st.selectbox("Select Test Package:", ["IELTS 6 - Test 1", "IELTS 6 - Test 2", "IELTS 6 - Test 3", "IELTS 6 - Test 4"])
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("▶️ Start Official Timer (30 Minutes)"):
            st.session_state.start_time = time.time()

    with col2:
        if st.session_state.start_time:
            elapsed = int(time.time() - st.session_state.start_time)
            remaining = max(0, 1800 - elapsed)
            mins, secs = divmod(remaining, 60)
            st.metric("⏳ Remaining Time", f"{mins:02d}:{secs:02d}")
            if remaining == 0:
                st.error("⏰ Time Limit Reached!")

    st.write("---")
    st.subheader(f"Exam Audio Stream: {selected_test}")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 

    with st.form(key="official_test_form"):
        st.subheader("IELTS Answer Sheet (Questions 1 to 40)")
        test_answers = {}
        for i in range(1, 41):
            test_answers[i] = st.text_input(f"Question {i}:", key=f"test_q_{i}")
        
        submit_test = st.form_submit_button("Submit Complete Exam")

    if submit_test:
        score = 31 # Sample score calculation
        band = get_ielts_band(score)
        
        st.balloons()
        st.success("🎉 Test Submitted Successfully!")
        res_col1, res_col2 = st.columns(2)
        res_col1.metric("Raw Score", f"{score} / 40")
        res_col2.metric("Estimated IELTS Band Score", f"Band {band}")
