% ΘΕΜΑ 1 - ΜΕΘΟΔΟΣ ΜΕΓΙΣΤΗΣ ΚΑΘΟΔΟΥ (Αλγόριθμος 5.2.1)
clc; clearvars; close all;

% Συνάρτηση f
f = @(x1, x2) (1/3)*x1^2 + 3*x2^2;

% Gradient της f
grad_f = @(x1, x2) [(2/3)*x1, 6*x2];

initial_point = [-10, 10 ]; % Αρχικό σημείο
gk = 5; % Σταθερό βήμα γκ 
epsilon = 0.001; % Ακρίβεια

% Υπολογισμοί
xk = initial_point; % Αρχικό σημείο
iter_cnt = 1; % Μετρητής επαναλήψεων
f_values = []; % Αποθήκευση τιμών της f για το plot σύγκλισης
       
while norm(grad_f(xk(1), xk(2))) > epsilon  
    % Αποθήκευση της τρέχουσας τιμής της f(x_k)
    f_values = [f_values, f(xk(1), xk(2))]; 
    gradf = grad_f(xk(1), xk(2)); % Υπολογισμός του gradient
    dk = -gradf; % Κατεύθυνση καθόδου

    % Ενημέρωση σημείου
    xk = xk + gk * dk;
    iter_cnt = iter_cnt + 1;      
end

% Αποθήκευση της τελικής τιμής της f(x_k)
f_values = [f_values, f(xk(1), xk(2))];

% Δημιουργία γραφήματος σύγκλισης
figure(1);
plot(1:length(f_values), f_values, 'LineWidth', 2, 'Color', 'b');
title(sprintf('Σύγκλιση για το αρχικό σημείο (%.1f, %.1f)', initial_point(1), initial_point(2)));
xlabel('Αριθμός επαναλήψεων');
ylabel('f(x_k)');
grid on;

% Εμφάνιση αποτελεσμάτων
fprintf('Αρχικό σημείο: (%.2f, %.2f)\n', initial_point(1), initial_point(2));
fprintf('Τελικό σημείο: x* = (%.4f, %.4f)\n', xk(1), xk(2));
fprintf('Τελική τιμή: f(x*) = %.6f\n', f(xk(1), xk(2)));
fprintf('Συνολικές επαναλήψεις: %d\n', iter_cnt - 1);