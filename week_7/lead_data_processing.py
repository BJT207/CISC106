from bakery import assert_equal
from lead import de_school_lead_samples as lead_data

"""
Global Vars
"""
#PPB (or ppb) stands for Parts Per Billion
SAMPLE1 = "0002ppb| Appoquinimink|               Alfred G Waters Middle School|Kitchen Faucet"
SAMPLE2 = "0002ppb|      Red Clay|                Forest Oak Elementary School|Nurse's Office Sink"
SAMPLE3 = "0008ppb|    Woodbridge|                    Woodbridge Middle School|Student Services Sink Faucet"

SAMPLES = [SAMPLE1,SAMPLE2,SAMPLE3]

"""
Helper Functions
"""
def count_samples(samples: list[str]) -> int:
    '''
    Takes in a list of samples and returns the number of samples in the list
    
    Args: 
        samples (list[str]): holds the list of samples
    Returns:
        int: number of samples
    '''
    
    return len(samples)
print("count_samples Tests:")
assert_equal(count_samples([]),0)
assert_equal(count_samples(["1","2"]),2)
assert_equal(count_samples(["1"]),1)
print("")

def total_lead(samples: list[str]) -> int:
    """
    Takes in a list of samples and returns the total lead in those sampels
    
    Args:
        samples (list[str]): lakes in the samples as a list of strings
    
    Returns:
        int: total pb of lead
    """
    total = 0
    if samples:
        for sample in samples:
            total += int(sample[0:4])
    return total

print("total_lead Tests:")
assert_equal(total_lead(SAMPLES),12)
assert_equal(total_lead(lead_data[0:4]),8)
assert_equal(total_lead([]),0)
print("")

def average_lead(samples: list[str]) -> float:
    '''
    Takes in a list of samples and returns the average lead across all samples in PPB
    
    Args:
        samples (list[str]): list of sample data
    Returns:
        float: average lead in PPB
    '''
    
    averagelead = 0.0
    numberofsamples = count_samples(samples)
    if numberofsamples:
        averagelead = total_lead(samples) / numberofsamples
    return averagelead

print("average_lead Tests:")
assert_equal(average_lead([]),0.0)
assert_equal(average_lead(SAMPLES),4.0)
assert_equal(average_lead(["0002","0002","0002"]),2.0)
print("")

def district_isolator(samples: list[str], district) -> list[str]:
    '''
    Takes in a list of samples and filters them by school district
    
    Args:
        samples (list[str]): a list of all the samples
        district (str): the district you want to filter for
    Return:
        list[str]: a list of the filtered samples
    '''
    filteredlist = []
    for sample in samples:
        if district in (((sample.split("|"))[1]).strip()):
            filteredlist.append(sample)
    return filteredlist

print("district_isolator Tests:")
assert_equal(district_isolator(SAMPLES,"Appoquinimink"), [SAMPLE1])
assert_equal(district_isolator(SAMPLES,"Red Clay"), [SAMPLE2])
assert_equal(district_isolator(SAMPLES,"Woodbridge"), [SAMPLE3])
print("")

def average_lead_per_district(samples: list[str], district: str) -> float:
    '''
    Takes in a list of samples and a school district and returns the average lead
    in ppm for that district
    
    Args:
        samples (list[str]): a list of all the samples
        district (str): string representing the district you want the average for
    Returns:
        float: a float representing the average ppm
    '''
    filterdlist = district_isolator(samples, district)
    return average_lead(filterdlist)

print("average_lead_per_district Tests:")
assert_equal(average_lead_per_district([],"test"),0.0)
assert_equal(average_lead_per_district(SAMPLES,"Appoquinimink"),2.0)
assert_equal(average_lead_per_district(SAMPLES+['0002ppb|    Woodbridge|                    Woodbridge Middle School|Water Bottle Filler Cafeteria'],"Woodbridge"), 5.0)
print("")
    
def highest_lead(samples: list[str]) -> int:
    '''
    Takes in a list of samples and finds the highest lead concentration
    
    Args:
        samples (list[str]): a list of all the samples
    Returns:
        int: the highest lead concentration
    '''
    highestlead = 0
    for sample in samples:
       if highestlead < int(sample[0:4]):
           highestlead = int(sample[0:4])
    return highestlead

print("highest_lead Tests:")
assert_equal(highest_lead([]),0)
assert_equal(highest_lead(SAMPLES),8)
assert_equal(highest_lead(SAMPLES+['0002ppb|    Woodbridge|                    Woodbridge Middle School|Water Bottle Filler Cafeteria']), 8)
print("")

def total_lead_per_district(samples: list[str], district: str) -> int:
    '''
    Filteres a sample set by district and sums up all the lead in that district
    Args:
        samples (list[str]): a list of all the samples
        district (str): the district you want to filter for
    Returns:
        int: the total of all the lead
    '''
    return total_lead(district_isolator(samples,district))

print("total_lead_per_district Tests:")
assert_equal(total_lead_per_district([],"test"),0)
assert_equal(total_lead_per_district(SAMPLES, "Appoquinimink"),2)
assert_equal(total_lead_per_district(SAMPLES+['0002ppb|    Woodbridge|                    Woodbridge Middle School|Water Bottle Filler Cafeteria'], "Woodbridge"), 10)
print("")

def school_isolator(samples: list[str], school:str) -> list[str]:
    '''
    Takes in a list of samples and filters them by school
    
    Args:
        samples (list[str]): a list of all the samples
        school (str): the school you want to filter for
    Return:
        list[str]: a list of the filtered samples
    '''
    filteredlist = []
    for sample in samples:
        if school in (((sample.split("|"))[2]).strip()):
            filteredlist.append(sample)
    return filteredlist

print("school_isolator Tests:")
assert_equal(school_isolator(SAMPLES,"Alfred G Waters Middle School"), [SAMPLE1])
assert_equal(school_isolator(SAMPLES,"Forest Oak Elementary School"), [SAMPLE2])
assert_equal(school_isolator(SAMPLES,"Woodbridge Middle School"), [SAMPLE3])
print("")

def total_lead_per_school(samples: list[str], school: str) -> int:
    '''
    Filteres a sample set by school and sums up all the lead in that school
    Args:
        samples (list[str]): a list of all the samples
        school (str): the school you want to filter for
    Returns:
        int: the total of all the lead
    '''
    return total_lead(school_isolator(samples,school))

print("total_lead_per_school Tests:")
assert_equal(total_lead_per_school([],"test"),0)
assert_equal(total_lead_per_school(SAMPLES, "Alfred G Waters Middle School"),2)
assert_equal(total_lead_per_school(SAMPLES+['0002ppb|    Woodbridge|                    Woodbridge Middle School|Water Bottle Filler Cafeteria'], "Woodbridge Middle School"), 10)
print("")

"""
Final Calculations
"""
print("")
print("Final Calculations")
print("------------------")
print("Number of Samples: " + str(count_samples(lead_data)) + " samples")
print("Total Lead: " + str(total_lead(lead_data))+ " PPB")
print("Average Lead Across All Samples: "+ str(average_lead(lead_data)) + " PPB")
print("Average Lead in Appoquinimink School District: " + str(average_lead_per_district(lead_data,"Appoquinimink")) + " PPB")
print("Average Lead in Red Clay School District: " + str(average_lead_per_district(lead_data,"Red Clay")) + " PPB")
print("Average Lead in Woodbridge School District: " + str(average_lead_per_district(lead_data,"Woodbridge")) + " PPB")
print("Highest Lead Sample: " + str(highest_lead(lead_data)) + " PPB")
print("Total Lead in Appoquinimink School District: " + str(total_lead_per_district(lead_data, "Appoquinimink")) + " PPB")
print("Total Lead in Woodbridge Middle School: " + str(total_lead_per_school(lead_data, "Woodbridge Middle School")) + " PPB")

