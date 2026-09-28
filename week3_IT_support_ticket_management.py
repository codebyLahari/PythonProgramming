"""
Description:
This program manages IT support tickets for an organization.
The user can create tickets, display tickets, search for tickets,
update ticket status, view high-priority tickets, and generate
a summary.

The program demonstrates Python lists, functions, loops,
decisions, searching, and list manipulation.
"""

def addTicket(ticketIDs, issues, priorities, statuses):
    ticketID = input("Enter Ticket ID: ")
    issue = input("Enter issue description: ")
    priority = input("Enter priority (High/Medium/Low): ")

    while priority.lower() not in ["high", "medium", "low"]:
        print("Invalid priority.")
        priority = input("Enter High, Medium, or Low: ")

    ticketIDs.append(ticketID)
    issues.append(issue)
    priorities.append(priority.title())
    statuses.append("Open")

    print("Ticket created successfully.")


def displayTickets(ticketIDs, issues, priorities, statuses):
    if len(ticketIDs) == 0:
        print("No support tickets available.")
        return

    print()
    print("---------- SUPPORT TICKETS ----------")

    for i in range(len(ticketIDs)):
        print("Ticket ID:", ticketIDs[i])
        print("Issue:", issues[i])
        print("Priority:", priorities[i])
        print("Status:", statuses[i])
        print("-------------------------------------")


def searchTicket(ticketIDs, issues, priorities, statuses):
    searchID = input("Enter Ticket ID to search: ")

    found = False

    for i in range(len(ticketIDs)):
        if ticketIDs[i].lower() == searchID.lower():
            print()
            print("Ticket Found")
            print("Ticket ID:", ticketIDs[i])
            print("Issue:", issues[i])
            print("Priority:", priorities[i])
            print("Status:", statuses[i])
            found = True

    if not found:
        print("Ticket not found.")


def updateTicketStatus(ticketIDs, statuses):
    searchID = input("Enter Ticket ID: ")
    found = False

    for i in range(len(ticketIDs)):
        if ticketIDs[i].lower() == searchID.lower():

            print("Current status:", statuses[i])
            newStatus = input("Enter new status (Open/In Progress/Closed): ")

            while newStatus.lower() not in ["open", "in progress", "closed"]:
                print("Invalid status.")
                newStatus = input(
                    "Enter Open, In Progress, or Closed: "
                )

            statuses[i] = newStatus.title()

            print("Ticket status updated.")
            found = True

    if not found:
        print("Ticket not found.")


def displayHighPriority(ticketIDs, issues, priorities, statuses):
    found = False

    print()
    print("----- HIGH PRIORITY TICKETS -----")

    for i in range(len(ticketIDs)):
        if priorities[i].lower() == "high":
            print(
                ticketIDs[i],
                "-",
                issues[i],
                "-",
                statuses[i]
            )
            found = True

    if not found:
        print("No high-priority tickets.")


def countOpenTickets(statuses):
    count = 0

    for status in statuses:
        if status.lower() != "closed":
            count = count + 1

    return count


def countClosedTickets(statuses):
    count = 0

    for status in statuses:
        if status.lower() == "closed":
            count = count + 1

    return count


def displaySummary(ticketIDs, priorities, statuses):
    print()
    print("---------- TICKET SUMMARY ----------")

    print("Total Tickets:", len(ticketIDs))
    print("Open Tickets:", countOpenTickets(statuses))
    print("Closed Tickets:", countClosedTickets(statuses))

    highPriority = 0

    for priority in priorities:
        if priority.lower() == "high":
            highPriority = highPriority + 1

    print("High Priority Tickets:", highPriority)


def main():

    ticketIDs = []
    issues = []
    priorities = []
    statuses = []

    choice = 0

    while choice != 7:

        print()
        print("===== IT SUPPORT TICKET SYSTEM =====")
        print("1. Create New Ticket")
        print("2. Display All Tickets")
        print("3. Search Ticket")
        print("4. Update Ticket Status")
        print("5. Display High Priority Tickets")
        print("6. Display Ticket Summary")
        print("7. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            addTicket(
                ticketIDs,
                issues,
                priorities,
                statuses
            )

        elif choice == 2:
            displayTickets(
                ticketIDs,
                issues,
                priorities,
                statuses
            )

        elif choice == 3:
            searchTicket(
                ticketIDs,
                issues,
                priorities,
                statuses
            )

        elif choice == 4:
            updateTicketStatus(
                ticketIDs,
                statuses
            )

        elif choice == 5:
            displayHighPriority(
                ticketIDs,
                issues,
                priorities,
                statuses
            )

        elif choice == 6:
            displaySummary(
                ticketIDs,
                priorities,
                statuses
            )

        elif choice == 7:
            print("Exiting IT Support Ticket System.")

        else:
            print("Invalid choice. Please select 1 through 7.")


main()
