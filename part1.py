import datetime



# Folder where files are stored
folder_path = "list"


# Read ManufacturerList.txt
f = open(folder_path + "\\ManufacturerList.txt", "r")
manufacturer_data = f.readlines()
f.close()

# Read PriceList.txt
f = open(folder_path + "\\PriceList.txt", "r")
price_data = f.readlines()
f.close()

# Read ServiceDatesList.txt
f = open(folder_path + "\\ServiceDatesList.txt", "r")
service_data = f.readlines()
f.close()

# Inventory dictionary to store all items
inventory = {}

# Process ManufacturerList.txt
for line in manufacturer_data:
    parts = line.strip().split(",")
    item_id = parts[0]
    manufacturer = parts[1].strip()
    item_type = parts[2].strip()
    damaged = "damaged" if len(parts) > 3 and parts[3].strip() == "damaged" else ""
    inventory[item_id] = {
        "manufacturer": manufacturer,
        "item_type": item_type,
        "damaged": damaged
    }

# Process PriceList.txt
for line in price_data:
    parts = line.strip().split(",")
    item_id = parts[0]
    price = parts[1].strip()
    if item_id in inventory:
        inventory[item_id]["price"] = price

# Process ServiceDatesList.txt
for line in service_data:
    parts = line.strip().split(",")
    item_id = parts[0]
    service_date = parts[1].strip()
    if item_id in inventory:
        inventory[item_id]["service_date"] = service_date

#FullInventory.txt (sorted by manufacturer)
items = list(inventory.items())

# sort by manufacturer 
n = len(items)
for i in range(n):
    for j in range(0, n-i-1):
        if items[j][1]["manufacturer"].lower() > items[j+1][1]["manufacturer"].lower():
            items[j], items[j+1] = items[j+1], items[j]

f = open(folder_path + "\\FullInventory.txt", "w")
for item_id, data in items:
    line = f"{item_id},{data['manufacturer']},{data['item_type']},{data['price']},{data['service_date']},{data['damaged']}".strip(",")
    f.write(line + "\n")
f.close()

# ItemTypeInventory files (sorted by ID) 
# Group items by type
type_groups = {}
for item_id, data in inventory.items():
    item_type = data['item_type']
    if item_type not in type_groups:
        type_groups[item_type] = []
    type_groups[item_type].append((item_id, data))

# Sort each type group by item ID 
for item_type, items in type_groups.items():
    n = len(items)
    for i in range(n):
        for j in range(0, n-i-1):
            if int(items[j][0]) > int(items[j+1][0]):
                items[j], items[j+1] = items[j+1], items[j]

    # Another folder path
    f = open(folder_path + f"\\{item_type}Inventory.txt", "w")
    for item_id, data in items:
        line = f"{item_id},{data['manufacturer']},{data['price']},{data['service_date']},{data['damaged']}".strip(",")
        f.write(line + "\n")
    f.close()


# Create PhoneInventory.txt (sorted by item ID)
if "phone" in type_groups:
    phone_items = type_groups["phone"]
    n = len(phone_items)
    for i in range(n):
        for j in range(0, n-i-1):
            if int(phone_items[j][0]) > int(phone_items[j+1][0]):
                phone_items[j], phone_items[j+1] = phone_items[j+1], phone_items[j]

    f = open(folder_path + "\\PhoneInventory.txt", "w")
    for item_id, data in phone_items:
        line = f"{item_id},{data['manufacturer']},{data['price']},{data['service_date']},{data['damaged']}".strip(",")
        f.write(line + "\n")
    f.close()






# PastServiceDateInventory.txt (sorted oldest to newest) 
today = datetime.datetime.now()
past_service_items = []

for item_id, data in inventory.items():
    service_date = datetime.datetime.strptime(data['service_date'], "%m/%d/%Y")
    if service_date < today:
        past_service_items.append((item_id, data, service_date))

# Sort by service date 
n = len(past_service_items)
for i in range(n):
    for j in range(0, n-i-1):
        if past_service_items[j][2] > past_service_items[j+1][2]:
            past_service_items[j], past_service_items[j+1] = past_service_items[j+1], past_service_items[j]

f = open(folder_path + "\\PastServiceDateInventory.txt", "w")
for item_id, data, service_date in past_service_items:
    line = f"{item_id},{data['manufacturer']},{data['item_type']},{data['price']},{data['service_date']},{data['damaged']}".strip(",")
    f.write(line + "\n")
f.close()

#DamagedInventory.txt (sorted most expensive to least expensive) 
damaged_items = [(item_id, data) for item_id, data in inventory.items() if data['damaged'] == 'damaged']

# Sort by price ( sort, highest first)
n = len(damaged_items)
for i in range(n):
    for j in range(0, n-i-1):
        if int(damaged_items[j][1]['price']) < int(damaged_items[j+1][1]['price']):
            damaged_items[j], damaged_items[j+1] = damaged_items[j+1], damaged_items[j]

f = open(folder_path + "\\DamagedInventory.txt", "w")
for item_id, data in damaged_items:
    line = f"{item_id},{data['manufacturer']},{data['item_type']},{data['price']},{data['service_date']}"
    f.write(line + "\n")
f.close()

print("All inventory files have been created successfully.")


# I am now free this took forever to do 
