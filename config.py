import numpy as np

valeurs_supprimer = [
    'NF','NC','NC ','NF ','fait , à recupérer','fait?',
    'en cours','en attente de nouvelles ','donneur',
    'FAIT à recupérer','NaT','fait, à récupérer','FAIT',
    'fait', 'en attente','fait ? ', 'fait? ','donneur (Belgique)',
    'donneur (Republique Tcheque)','DONNEUR',' ','na','à récupérer',
    'B','A COMPLETER UNE FOIS PGS FAIT','4 (?)','enceinte ','enceinte',
    'à compléter','à terme','patiente enceinte (32SA), à compléter','NaT'
    'enceinte, infos à compléter','œuf clair','en cours de récupération',
    'en cours? ','fait à limoges? À récupérer','N1','à récupérer','EN COURS',
    'en cours?','en cours ?','fait ? À récupérer','CR à récupérer','en cours !',
    'en cours de relecture','demande de relecture','poids à récupérer','à récupérer ',
    'à recupérer','à récupérer','sexe à récupérer',"à maintenir jusqu'à accouchement",
    'tjr en cours','le jour du transfert','NA pas de grossesse obtenue','Donneur','nf','nc',
    'enceinte, infos à compléter'
]

colonnes_supprimer_avant_encodage= [
    'Project','detailled medical conditions',
    'Unnamed: 109','Weight (kg)','Height (in m)',
    'identification (initials 3 letters of the surname)',
    'Department (France) or Country','Referring doctor_City',
    'Level of education_none0_CAPBEP/GCSE_1_BAC/A Levels_2_BAC+2/Undergrad_3_supBAC+2/Postgrad_4',
    'Tea/Coffee_No 0_Yes(nbcups/day)','SpecificDiet_none0_vegetarian1_vegan2_other3',
    'BaeckePhysical Activity questionnaire_score','date of surgery for endometriosis',
    'endometrial thickness(in mm)_D21','endometrial volume (cm3)',
    'NON-CONVENTIONAL ANTIPHOSPHOLIPID ANTIBODIES (if positive precise which ones)',
    'FSH_D3','LH_D3','E2_D3','hypertestosteronemia/D4A Yes1_No0','HLA KIR LYON_patient',
    'HLA KIR LYON_partner',' antiHLA antibodies St Louis','Matricelab test_month_year',
    'MatriceLab_normal0_underactivation1_overactivation2_mix3',
    'spermDNA fragmentation_Normal< 30% 0_abnormal1','congenital malformation_yes1_no0',
    'birth complications (Premature rupture of membranes _1 or premature delivery threat_2 hemorrhage_3)',
    'Placental hypertrophy_yes1_no2','Placenta_CHI1_infarcts2_chorioamniotitis3_hypoxia4_villitis5',
    'Weight_Child1_g','Sex Child1_girl1 _boy2','Weight_Child2_g','Sex Child2_girl1 _boy2',
    'IL2_out of study1_ FACIL2 study 2','other no=0, or plain text','PSSScore 1stconsultation',
    'Stress management tools_0none_plain text','PSSScore start of pregnancy','biocollection ',
    'Latest follow up date','Level of education_none0_CAPBEP/GCSE_1_BAC/A Levels_2_BAC+2/Undergrad_3_supBAC+2/Postgrad_4.1',
    'PSSScore 1stconsultation','Stress management tools_0none_plain text',
    'Latest follow up date','Unnamed: 109','Project','WIN /ERA\ntest_normal0_ifnotplaintext'
]
colonne_renomer  = {
    'Ethnicity_Europe1_NorthAfrica2_Sub saharan Africa3_Overseas France South America4_Asia5':'Ethnicity',
    'Medical conditions: none=0 Auto immune =1 Thromboembolic = 2 \nOther = 3':'Medical conditions',
    'cause of infertility tubal =1, masculine =2, ovarian =3 PCOS=4 unexplained=5':'Cause of infertility',
    'miscarriage_1_ livebirth_2_\nabortion_3_\ntermination_4_sup12SA_5':'Miscarriage ou autre',
    'Pregnancy complications_hypertension_1 fœtal death 2 _Retroplacental hemorrhage3_gesta diab_4_Oligohydramnios_5_hyperemesis gravidarum6 _PEE7_Intrauterine Growth Restriction8':'Pregnancy complications',
    'CONVENTIONAL ANTIPHOSPHOLIPID ANTIBODIES (if positive precise which ones)':'Conventional antiphospholipid'

}

fill_conditions = [
    {
        'condition_col': 'Endometriosis no 0_yes1',
        'values': [0],
        'target_cols': ['Deeply infiltrating endometriosis yes1_no2', 'If yes, surgery? Yes1_no2'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'TECHNIQUE_ spontaneous pregnancy1_ InducedOvulation2_IUI3_ IVF4_ICSI5_ IMSI6',
        'values': [1, 2, 3, 6],
        'target_cols': ['PGS_Yes1_No0', 'PGS result'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'Pregnancy_yes1_no0',
        'values': [0],
        'target_cols': ['Pregnancy complications'],
        'nouvelle_valeur': 'Pas enceinte'
    },
     {
        'condition_col': 'Miscarriage ou autre',
        'values': [2],
        'target_cols': ['karyotype miscarriage test_Notdone0_normal1_abnormal2'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'Pregnancy_yes1_no0',
        'values': [0],
        'target_cols': ['karyotype miscarriage test_Notdone0_normal1_abnormal2'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'Pregnancy_yes1_no0',
        'values': [0],
        'target_cols': ['Termoftheevent_weeks of amenorrhea'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'Prednisone no=0 , if yes dosage in mg',
        'values': [0],
        'target_cols': ['Prednisone stop date in weeks of amenorrhea'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'Hydroxychloroquine_No0_pre conception1_during pregnancy2 ',
        'values': [0],
        'target_cols': ['Hydroxychloroquine stop date in weeks of amenorrhea'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'Intralipid__No0_pre conception1_during pregnancy2 ',
        'values': [0],
        'target_cols': ['Intralipid stop date in weeks of amenorrhea'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'Adalimumab__No0_pre conception1_during pregnancy2',
        'values': [0],
        'target_cols': ['Adalimumab stop date in weeks of amenorrhea'],
        'nouvelle_valeur': 0
    },
    {
        'condition_col': 'TECHNIQUE_ spontaneous pregnancy1_ InducedOvulation2_IUI3_ IVF4_ICSI5_ IMSI6',
        'values': [1, 2, 3],
        'target_cols': ['Nb_emb_transferred', 'Ageofembryo_D3_1_D5_2'],
        'nouvelle_valeur': 0
    }
]

replacement_conditions = [
    {
        'column': 'ANA pattern',
        'replacement_dict': {
            1: ['sans spécificité', 'sans spécificté', 'positifs sur cellules HEp-2', 'Ac anti-RNP ', 
                'Ac anti-CPG positifs > 1/160', 'AAN', 'anti facteur intrinsèque et anti cellules pariétales gastriques positifs',
                'anti ARN POL 3 à 30 UI/L ', 'ANCA à 1/640 de type cANCA sans spécificité; de nouveau positif à 1/640e',
                'anti ARN POL 3 pos à 56', 'anti ADN positif à 11 ', 'anti ADN positif à 28'],
            2: ['anti SSA positif', ' de type anti SSA Ro52 et Ro60', 'avec anti SSA/Ro60 positifs', 
                'anti SSB positifs ', 'AC anti centromère taux très élevé , Ac anti-SSA (Ro) 52kDa positifs. Ac anti-SSa 60 kDa positifs',
                'anti SSB isoléments positifs', 'anti-SSA Ro52KDA', ' Ac anti-SSa 60 kDa positifs.', 'type anti SSA RO60 et DFS70'],
            3: ['anticentromères positifs.', 'AC anti centromère et anti Pm Scl faiblement positifs', 
                'anti centromère, anti MDA5 positif', 'anti PM scl100 positif']
        }
    },
    {
        'column': 'PGS result',
        'replacement_dict': {
            1: ['normal'],
            2: ['anormal, conjoint a une translocation chromosomique ', "2 normaux sur les 3J5 dont un transféré du fait d'une incompatibilité HLA Kir inhibiteur ",
                'sur les 3 embryons, 2 euploïdes'],
            np.nan: ['aucun embryon transférable']
        }
    }
]

all_mappings = {
    'Implantation Failure =1 Reccuring miscarriages = 2': {
         1 : ['Implantation_Failure'],
        '1 et 2': ['Implantation_Failure', 'Reccuring_miscarriages'],
        '1 ET 2': ['Implantation_Failure', 'Reccuring_miscarriages'],
         2 : ['Reccuring_miscarriages']
    },
    'Ethnicity':{
         1 : ['Ethnicity_Europe'],
         2 : ['NorthAfrica'],
         3 : ['Sub_saharan_Africa'],
         4 : ['Overseas_France_South_America'],
         5 : ['Asia'],
        '1 et 5': ['Ethnicity_Europe', 'Asia'],
        '1 et 2': ['Ethnicity_Europe', 'NorthAfrica']
    },
    'Medical conditions':{
         0 : ['Pas_de_Medical_condition'],
         1 : ['Auto_imune'],
         2 : ['Thromboembolic'],
         3 : ['other_Medical_condition'],
        '1 et 2': ['Auto_imune', 'Thromboembolic']
    },
    'Cause of infertility':{
         1 : ['Cause_infertility_tubal'],
         2 : ['Cause_infertitlity_masculine'],
         3 : ['Cause_infertility_ovarian'],
         4 : ['Cause_infertility_PCOS'],
         5 : ['Cause_infertility_unexplained'],
        '2.4': ['Cause_infertitlity_masculine', 'Cause_infertility_PCOS'],
        '1 and 4': ['Cause_infertility_tubal', 'Cause_infertility_PCOS'],
        '2 , 3': ['Cause_infertitlity_masculine', 'Cause_infertility_ovarian']

    },
    'Miscarriage ou autre':{
         1 : ['Miscarriage'],
         2 : ['Livebirth'],
         3 : ['Abortion'],
         4 : ['Termination'],
        '1 et 2': ['Miscarriage', 'Livebirth'],
        'pas enceinte': [],
        'Autre': ['Autre_methode']
    },
    'Pregnancy complications':{
     0 : ['Pas_de_complications'],
     1 : ['Hypertension'],
     2 : ['Fœtal_death'],
     3 : ['Retroplacental_hemorrhage'],
     4 : ['gesta_diab'],
     5 : ['Oligohydramnios'],
     6 : ['hyperemesis_gravidarum'],
     7 : ['PEE'],
     8 : ['Intrauterine_Growth_Restriction'],
    'Autre_complication': ['Autre_complication'],
    '1, 2': ['Hypertension', 'Fœtal_death'],
    '1,3 et 8': ['Hypertension', 'Retroplacental_hemorrhage', 'Intrauterine_Growth_Restriction'],
    '1 , 4': ['Hypertension', 'gesta_diab'],
    '2 et 3': ['Fœtal_death', 'Retroplacental_hemorrhage'],
    '2, 3': ['Fœtal_death', 'Retroplacental_hemorrhage'],
    '2 , 3': ['Fœtal_death', 'Retroplacental_hemorrhage'],
    '2, 6': ['Fœtal_death', 'hyperemesis_gravidarum'],
    '2, 4': ['Fœtal_death', 'gesta_diab'],
    '2 , 4, 8': ['Fœtal_death', 'gesta_diab', 'Intrauterine_Growth_Restriction'],
    '2, 5': ['Fœtal_death', 'Oligohydramnios'],
    '2, 3, 7, 8': ['Fœtal_death', 'Retroplacental_hemorrhage', 'PEE', 'Intrauterine_Growth_Restriction'],
    '2, 7': ['Fœtal_death', 'PEE'],
    '1, 2, 5': ['Hypertension', 'Fœtal_death', 'Oligohydramnios'],
    '1, 5': ['Hypertension', 'Oligohydramnios'],
    '4, 7': ['gesta_diab', 'PEE'],
    '3, 7, 8': ['Retroplacental_hemorrhage', 'PEE', 'Intrauterine_Growth_Restriction'],
    '2, 8': ['Fœtal_death', 'Intrauterine_Growth_Restriction'],
    '5, 7 et thrombopénie': ['Oligohydramnios', 'PEE'], 
    '2, 7, 8': ['Fœtal_death', 'PEE', 'Intrauterine_Growth_Restriction'],
    '1 ET 4': ['Hypertension', 'gesta_diab'],
    '5, 8': ['Oligohydramnios', 'Intrauterine_Growth_Restriction'],
    '5 et 8': ['Oligohydramnios', 'Intrauterine_Growth_Restriction'],
    '8 et anomalie du rythme cardiaque fœtal': ['Intrauterine_Growth_Restriction'], 
    '7, 8': ['PEE','Intrauterine_Growth_Restriction'],
    '3 , 5, 7 , 8': ['Retroplacental_hemorrhage','Oligohydramnios','PEE','Intrauterine_Growth_Restriction'],
    '1 , 3 , 4': ['Hypertension','Retroplacental_hemorrhage','gesta_diab'],
    '2 et 4':['Fœtal_death','gesta_diab'],
    'Pas enceinte':['Pas_de_complications'],
    '1,3 et 8 ': ['Hypertension','Retroplacental_hemorrhage','Intrauterine_Growth_Restriction']

    }

}

replacements_manuelle = {
    'Termoftheevent_weeks of amenorrhea': {
        '8-9': 9,
        '3-4': 4,
        '29 + 5': 34,
        '40 + 5': 45,
        '4 (sd hyperstim)': 4,
        '28 SA NV + MFIU 25 SA': 25,
        'NC (< premier trimestre)': 7,
        'GLI': np.nan,
        '12 ': 12
    },
    'Prednisone stop date in weeks of amenorrhea': {
        "8 SA baissé à 10mg puis décroissance jusqu'à arrêt total environ 12SA": 12,
        "jusqu'à fin grossesse": 40,
        'jusqu’à fin grossesse': 40,
        "commencé à 23SA pour RCIU, continué jusqu'à fin grossesse ": 40,
        "commencé à 8SA stop 14SA": 14
    },
    'Hydroxychloroquine stop date in weeks of amenorrhea': {
        'jusqu’à fin grossesse': 40,
        "STOP à 3SA à cause d'un urticaire": 3,
        "jusqu'à fin grossesse": 40,
        'maintenu 6 semaines post partum': 46,
        '22  ?': 22
    },
    'Adalimumab stop date in weeks of amenorrhea': {
        'EI': np.nan,
        '8 SA?': 8,
        'pas de transfert car mauvaise qualité embryonnaire ': 0,
        'pas de grossesse obtenue après deux inséminations': 0,
        'échec insem': 0,
        '9 puis repris à 18SA pour RCIU': np.nan,
        'GEU': np.nan
    },
    'Prednisone no=0 , if yes dosage in mg': {
        '10 puis 20': 20,
        '20 puis 10': 10,
        '10 puis 5': 5
    },
    'PGS result': {
        'anormal, conjoint a une translocation chromosomique ': 'anormal',
        "2 normaux sur les 3J5 dont un transféré du fait d'une incompatibilité HLA Kir inhibiteur ": 'anormal',
        'aucun embryon transférable': np.nan,
        'sur les 3 embryons, 2 euploïdes': 'anormal'
    },
    'Intralipid stop date in weeks of amenorrhea': {
        'uniquement en préconceptionnel': 0,
        'juste préconceptionnel': 0,
        'préconceptionnel': 0,
        'Echec stim': 0,
        '3 SA GEU': 3,
        '2 jours avant transfert puis 9 jours après le transfert': 1,
        '5?': 5,
        'uniquement à 6SA': 6,
        'unique perfusion à 5SA': 5,
        'EI': np.nan
    },
    'Prednisone no=0 , if yes dosage in mg': {
        '10 puis 20': 20,
        '20 puis 10': 10,
        '10 puis 5': 5
    }
}

replacements_pregnancy_complication = {
    '2 et 5': '2, 5',
    'N0': np.nan,
    'hydramnios': 'Autre_complication',
    'élévation PAL, souffrance fœtale, RCIU': 'Autre_complication',
    'cytolyse, thrombopénie': 'Autre_complication',
    'thrombopénie gestationnel': 'Autre_complication',
    'cholestase gravidique ': 'Autre_complication',
    'hospitalisation pour vomissement incoercible, cholestase, élévation des PAL': 'Autre_complication',
    'cholestase gravidique': 'Autre_complication',
    'hypothyroïdie non auto immune': 'Autre_complication',
    "allo immunisation anti E ( RH3) faible suivie au CNRHP. Conjoint E négatif. Pas d'incompatibilité.": 'Autre_complication',
    '1,5 mois de grossesse hématome décidual, résorbé / 7 mois de grossesse TVP sans ttt anticoagulant': '1, 5'
}
