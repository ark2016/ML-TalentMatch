from pyresparser import ResumeParser



def main():
    data = ResumeParser("C:/Users/edelk/Gitflic/GitHub/ML-TalentMatch/resume/Akhundov Damat.pdf").get_extracted_data()
    print(data, "ds")

main()