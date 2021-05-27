Get-ADGroupMember "GWD-RDS-GFBIO-User" | Get-ADUser -Properties EmailAddress | select UserPrincipalName, Name | Export-Csv 'C:\WebServer\dwb-hosting-concept\domain_users.csv' -NoType
