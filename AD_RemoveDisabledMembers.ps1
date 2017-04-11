###
### Script will find disabled users in your AD Container, and remove their memberships from groups
### Need to be run with a user who has admin privileges in AD for this container
###

# Ou to look for users
$OU = “OU=USERS,dc=addomain,dc=com”

# Looking for users, export to CSV. Easier if you want to review
Get-ADUser -SearchBase $OU -Filter * | Select SamAccountName,Enabled | export-csv adusers_status.csv

# Removing users if status of Enabled == "False"
import-csv adusers_status.csv | foreach { if ($_.Enabled -eq "False") { Get-ADPrincipalGroupMembership $_.SamAccountName | Remove-ADGroupMember -Member $_.SamAccountName } } 

###
### Can be done in 1 line
###

# Get-ADUser -SearchBase $OU -Filter * | Select SamAccountName,Enabled | foreach { if ($_.Enabled -eq "False") { Get-ADPrincipalGroupMembership $_.SamAccountName | Remove-ADGroupMember -Member $_.SamAccountName } } 