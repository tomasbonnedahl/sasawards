before = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>SAS Awards</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="margin: 0; padding: 0;">
<table border="0" cellpadding="40" cellspacing="0" width="100%">
    <tr>
        <td>
            <table align="center" border="1" cellpadding="10" cellspacing="0" width="400"
                   style="border-collapse: collapse;">
                <tr>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px;">
                        <b>From</b>
                    </td>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px;">
                        <b>To</b>
                    </td>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px;">
                        <b>Departure</b>
                    </td>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px;">
                        <b>Business seats</b>
                    </td>
                </tr>
'''

mid = '''<tr>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px; line-height: 20px;">
                        {origin}
                    </td>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px; line-height: 20px;">
                        {to}
                    </td>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px; line-height: 20px;">
                        {date}
                    </td>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px; line-height: 20px;">
                        {business_seats}
                    </td>
                </tr>
'''

after = '''            </table>
        </td>
    </tr>
</table>
<table border="0" cellpadding="20" cellspacing="0" width="100%">
    <tr>
        <td>
            <table align="center" border="0" cellpadding="5" cellspacing="0" width="180"
                   style="border-collapse: collapse;">
                <tr>
                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 18px;">
                        <a href="https://thawing-ravine-34523.herokuapp.com/flights/">Click to view seats</a>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</body>
</html>

'''