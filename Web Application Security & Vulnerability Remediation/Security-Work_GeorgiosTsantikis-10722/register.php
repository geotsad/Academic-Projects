<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Form</title>
</head>
<body>
    <h3>New user registration</h3>

<?php
// Ονοματεπώνυμο : Γεώργιος Τσαντίκης
// ΑΕΜ : 10722
// Email : tsangeor@ece.auth.gr


// Resume existing session (or start a new one)
session_start();

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true && $_SESSION['username'] !== '') {
	echo "<font color=red>You are already logged in!</font></br>";
	echo "Please <a href='logout.php'>logout</a> first";
    exit;
}

// --- ΣΥΝΑΡΤΗΣΗ HASHING ---
function getPasswordHash_Hex($username, $password) {
    $salt = hash('sha256', $username); // Δημιουργία salt από το username
    $saltedPwd = $salt . $password;
    $hashedPwd = hash('sha256', $saltedPwd);
    return ['hash' => $hashedPwd, 'salt' => $salt];
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
	if(!isset($_POST['new_username'], $_POST['new_password']) || trim($_POST['new_username']) =='' || trim($_POST['new_password']) == '') {
		$login_message = "Missing username or password.";
	}
	else {
		$new_username = trim($_POST['new_username']);
		$new_password = trim($_POST['new_password']);

		mysqli_report(MYSQLI_REPORT_OFF);
		$conn=mysqli_connect("localhost","root","","pwd_mgr");
		if (mysqli_connect_errno())	{ echo "Failed to connect: " . mysqli_connect_error(); exit(); }

        // Έλεγχος αν υπάρχει ο χρήστης
        $checkStmt = $conn->prepare("SELECT id FROM login_users WHERE username = ?");
        $checkStmt->bind_param("s", $new_username);
        $checkStmt->execute();
        $checkStmt->store_result();

        if ($checkStmt->num_rows > 0) {
            $login_message = "Error, user already exists!";
        } else {
            // Hashing του κωδικού
            $securityData = getPasswordHash_Hex($new_username, $new_password);
            $hashedPwd = $securityData['hash'];
            $salt = $securityData['salt'];

            // Εισαγωγή στη βάση
            $insertStmt = $conn->prepare("INSERT INTO login_users (username, password, salt) VALUES (?, ?, ?)");
            $insertStmt->bind_param("sss", $new_username, $hashedPwd, $salt);

            if ($insertStmt->execute()) {
                echo "<font color=red>Successful registration!</font>";
                echo "<p />You can now use the <a href='login.php'>login</a> page";
                exit;
            } else {
                $login_message = "Error during registration.";
            }
            $insertStmt->close();
        }
        $checkStmt->close();
		$conn -> close();
	}
}
?>

<body>
	<p/>
	<form method="POST" action="register.php">
        <input type="text" name="new_username" placeholder="Username"><br />
        <input type="password" name="new_password" placeholder="Password"><br />
        <button type="submit">Register</button>
    </form>

	<br />

    <?php
		if (!empty($login_message)) { 
			echo "<font color=red>$login_message</font>";
			echo "<p />Go to the <a href='login.php'>login</a> page";
		}
	?>

</body>
</html>