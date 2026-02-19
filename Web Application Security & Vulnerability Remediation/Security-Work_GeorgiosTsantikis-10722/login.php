<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
</head>

<?php
// Ονοματεπώνυμο : Γεώργιος Τσαντίκης
// ΑΕΜ : 10722
// Email : tsangeor@ece.auth.gr


// Start a new session (or resume an existing one)
session_start();

// Check if the user is already logged in
if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true && $_SESSION['username'] !== '') {
    header("Location: dashboard.php");
    exit;
}

function getPasswordHash_Hex($username, $password) {
    $salt = hash('sha256', $username);
    $saltedPwd = $salt . $password;
    $hashedPwd = hash('sha256', $saltedPwd);
    return ['hash' => $hashedPwd, 'salt' => $salt];
}

// Συναρτήσεις για το κλειδί κρυπτογράφησης
function getPasswordHash_Bin($username, $password) {
    $salt = hash('sha256', $username, true);
    $saltedPwd = $salt . $password;
    return ['hash' => hash('sha256', $saltedPwd, true), 'salt' => $salt];
}
function deriveEncryptionKey($username, $password) {
    $pwdHash = getPasswordHash_Bin($username, $password);
    return hash_pbkdf2('sha256', $pwdHash['hash'], $pwdHash['salt'], 100000, 32, true);
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
	if(!isset($_POST['username'], $_POST['password']) || trim($_POST['username']) =='' || trim($_POST['password']) == '') {
		$login_message = "Missing username or password.";
	}
	else {
		$username = trim($_POST['username']);
		$password = trim($_POST['password']);

		$conn=mysqli_connect("localhost","root","","pwd_mgr");
		if (mysqli_connect_errno())	{ echo "Failed to connect: " . mysqli_connect_error(); exit(); }

		// SQL Injection Fix
		$stmt = $conn->prepare("SELECT id, password, salt FROM login_users WHERE username=?");
		$stmt->bind_param("s", $username);
		$stmt->execute();
		$result = $stmt->get_result();

		if ($row = $result->fetch_assoc()) {
            // Verify Hash
            $securityData = getPasswordHash_Hex($username, $password);
            
			if ($securityData['hash'] === $row['password']) {
				$_SESSION['username'] = $username;
				$_SESSION['loggedin'] = true;
                // Αποθήκευση κλειδιού για το Dashboard
                $_SESSION['secret_key'] = deriveEncryptionKey($username, $password);

				header("Location: dashboard.php");
				exit;
			} else {
				$login_message = "Invalid username or password";
			}
		} else {
			$login_message = "Invalid username or password";
		}
		$stmt->close();
		$conn -> close();
	}
}
?>

<body>
    <h3>Password Manager</h3>
    <form method="POST" action="">
        <input type="text" name="username" placeholder="Username" required><br />
        <input type="password" name="password" placeholder="Password"><br />
        <button type="submit">Login</button>
    </form>
	<br />
    <?php if (!empty($login_message)) { echo "<font color=red>$login_message</font>"; } ?>
	<p/>
    <a href="register.php">Register new user</a>
	<p/>
	<a href="index.html">Home page</a>
</body>
</html>