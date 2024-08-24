from agency_swarm import Agency
from TourGuideAgency.TourGuide import TourGuide

def init_agency():
    tour_guide = TourGuide()
    agency = Agency([tour_guide],
                    max_prompt_tokens=25000,  # default tokens in conversation for all agents
                    temperature=0.3,  # default temperature for all agents
                    shared_files=['./fsq-categories.csv']
                    )
    agency.shared_state.set('finished', False)
    return agency

if __name__ == '__main__':
    agency = init_agency()
    agency.demo_gradio()