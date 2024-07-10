# -*- coding: utf-8 -*-
"""

@author: puser
CRUD - staff information 
"""
###index.php 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Staff Management</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        form {
            width: 400px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="text"], input[type="email"], select {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            float: right;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h2>Staff Management</h2>
    
    <form action="process.php" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br>
        
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br>
        
        <label for="position">Position:</label>
        <select id="position" name="position" required>
            <option value="Manager">Manager</option>
            <option value="Developer">Developer</option>
            <option value="Designer">Designer</option>
        </select><br>
        
        <input type="submit" value="Add Staff">
    </form>

    <hr>
    <h3>Current Staff</h3>
    <ul>
        <?php
        // to fetch and display current staff from the database
        $db = oci_connect('username', 'password', 'oracle_connection_string');
        
        if (!$db) {
            $e = oci_error();
            trigger_error(htmlentities($e['message'], ENT_QUOTES), E_USER_ERROR);
        }
        
        $query = 'SELECT * FROM staff';
        $stmt = oci_parse($db, $query);
        oci_execute($stmt);
        
        while ($row = oci_fetch_assoc($stmt)) {
            echo '<li>' . $row['NAME'] . ' - ' . $row['EMAIL'] . ' - ' . $row['POSITION'] . '</li>';
        }
        
        oci_free_statement($stmt);
        oci_close($db);
        ?>
    </ul>
</body>
</html>

###process.php 
import cx_Oracle

class StaffManagement:
    def __init__(self):
        self.connection = cx_Oracle.connect('username', 'password', 'oracle_connection_string')
        self.cursor = self.connection.cursor()

    def add_staff(self, name, email, position):
        sql = 'INSERT INTO staff (name, email, position) VALUES (:1, :2, :3)'
        self.cursor.execute(sql, (name, email, position))
        self.connection.commit()

    def fetch_staff(self):
        sql = 'SELECT * FROM staff'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

# Process incoming POST request from PHP
if __name__ == '__main__':
    import cgi
    form = cgi.FieldStorage()
    
    name = form.getvalue('name')
    email = form.getvalue('email')
    position = form.getvalue('position')
    
    if name and email and position:
        staff_manager = StaffManagement()
        staff_manager.add_staff(name, email, position)
        del staff_manager
    
    # Redirect back to index.php after adding staff
    print('Location: index.php')
    print('')




