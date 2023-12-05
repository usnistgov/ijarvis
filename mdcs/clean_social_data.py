"""Get social account data and remove unecessary fields."""
import json, pprint

json_name = "social_users.json"
json_name_out = "social_users1.json"

with open(json_name, "r") as f:
    data = json.load(f)

# pprint.pprint(data)
# print (data,len(data))


def nullify_keys(entry={}):
    keys_google = ["picture", "locale"]
    keys_microsoft = [
        "businessPhones",
        "mobilePhones",
        "jobTitle",
        "officeLocation",
        "preferredLanguage",
    ]
    keys_github = [
        "avatar_url",
        "gravatar_id",
        "company",
        "blog",
        "location",
        "hireable",
        "bio",
        "twitter_username",
        "followers",
        "following",
    ]
    all_keys = keys_google + keys_microsoft + keys_github
    for i in all_keys:
        try:
            if i in entry:
                entry[i] = ""
        except:
            pass
    return json.dumps(entry)


mem = []
for i in data:
    if i["fields"]["provider"] == "google":
        extra_data = json.loads(i["fields"]["extra_data"])
        extra_data = nullify_keys(extra_data)
        i["fields"]["extra_data"] = extra_data

    if i["fields"]["provider"] == "microsoft":
        extra_data = json.loads(i["fields"]["extra_data"])
        extra_data = nullify_keys(extra_data)
        i["fields"]["extra_data"] = extra_data
    if i["fields"]["provider"] == "github":
        extra_data = json.loads(i["fields"]["extra_data"])
        extra_data = nullify_keys(extra_data)
        i["fields"]["extra_data"] = extra_data
    mem.append(i)

with open(json_name_out, "w") as f:
    f.write(json.dumps(mem, indent=1))
