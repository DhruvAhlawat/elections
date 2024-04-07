import json

with open('voters.jsonl', 'r') as f:
    all_voters = [json.loads(line) for line in f]

candidates = ['duds', 'daddu', 'daddy', 'rajjs']; #Candidate list.

def verify_voters(voters, candidates, total_preferences=3):
    # Check if the preferences are in the candidates list.
    for i in range(len(voters)):
        if(len(set(voters[i]['preferences'])) != total_preferences):
            print("Error, the number of preferences for voter", i+1, "is not equal to", total_preferences);
            print("Please provide exactly", total_preferences, "preferences for each voter (without repetition).");
            return False;
        for j in range(len(voters[i]['preferences'])):
            if voters[i]['preferences'][j] not in candidates:
                print("Error, Did you spell the name'", voters[i]['preferences'][j] ,"'correctly (with correct case as put in candidates list)?");
                print("names in preference list must be from the list: ", candidates);
                return False;
    return True;


def get_first_preferences_count(candidates, voters):
    # Create a dictionary to store the number of votes each candidate has
    votes = {candidate: 0 for candidate in candidates}
    # iterate over each voters's preferences.
    for i in range(len(voters)):
        first_preference = voters[i]['preferences'][0]
        try:
            votes[first_preference] += 1;
        except Exception as e:
            print("Error, Did you spell the name'", first_preference ,"'correctly (with correct case as put in candidates list)?");
            print("Error: ", e);    
    return votes

def get_full_votes(candidates, voters, prefnum=1):
    # first we count the values and get the lowermost value and eliminate it.
    initial_votes = get_first_preferences_count(candidates, voters);
    print("Initial", prefnum, "preference votes: ", initial_votes);
    lowest_value = min(initial_votes.values());
    # Get the candidate with the lowest value.
    lowest_candidate = [key for key in initial_votes if initial_votes[key] == lowest_value];
    print("Lowest candidate(s): ", lowest_candidate, "with", lowest_value, "votes.");
    if(len(lowest_candidate) != 1):
        print("more than one lowest candidate, edge case not handled.");
    
    # Eliminate the lowest candidate.
    if(len(voters[0]['preferences']) == 1):
        return initial_votes; #get the votes that we have at the end.
    for i in range(len(voters)):
        if(lowest_candidate[0] in voters[i]['preferences']):
            for j in range(len(voters[i]['preferences'])):
                if voters[i]['preferences'][j] == lowest_candidate[0]:
                    voters[i]['preferences'].pop(j); #popping the j'th position.
                    break;
        else:
            voters[i]['preferences'].pop(); #popping the last preference otherwise so all the preferences are of the same size now.
    #now we remove the lowest candidate.
    candidates.remove(lowest_candidate[0]);
    return get_full_votes(candidates, voters, prefnum+1);
    # now we have removed the last candidate from the list.

    # Now we repeat the process.
    
num_preferences = 3;
if(not verify_voters(all_voters, candidates, num_preferences)):
    print("exiting...");
    exit(0) #verifies whether all voters have the correct number of preferences.

final_votes = get_full_votes(candidates, all_voters); #get the final votes after eliminating the lowest candidates.

print(final_votes); #print the final votes.
