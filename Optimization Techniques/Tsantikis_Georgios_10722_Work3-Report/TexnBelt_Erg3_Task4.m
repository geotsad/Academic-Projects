% ΘΕΜΑ 4 - ΜΕΘΟΔΟΣ ΜΕΓΙΣΤΗΣ ΚΑΘΟΔΟΥ με ΠΡΟΒΟΛΗ
% για αρχικό σημείο (8, -10)
clc; clearvars; close all;

% Συνάρτηση f
f = @(x1, x2) (1/3)*x1^2 + 3*x2^2;

% Gradient της f
grad_f = @(x1, x2) [(2/3)*x1, 6*x2];

initial_point = [8, -10]; % Αρχικό σημείο
sk = 0.1; % Σταθερό βήμα sκ της μεθ. Μέγιστης Καθόδου
gk = 0.2; % Σταθερό βήμα γκ της μεθ. Εφικτών Κατευθύνσεων για την προβολή
epsilon = 0.01; % Ακρίβεια
lower_bounds = [-10, -8];
upper_bounds = [5, 12];
max_iter=1000;

% Συνάρτηση προβολής στο ορθογώνιο σύνολο περιορισμών
projection = @(x) max(lower_bounds, min(upper_bounds, x));

% Αρχικοποίηση
xk = initial_point; % Σημείο εκκίνησης
iter_cnt = 1; % Μετρητής επαναλήψεων
f_values = []; % Αποθήκευση τιμών της f για το γράφημα σύγκλισης

while norm(grad_f(xk(1), xk(2))) > epsilon && iter_cnt < max_iter
    % Υπολογισμός της κατεύθυνσης καθόδου
    gradf = grad_f(xk(1), xk(2));
    dk = -gradf; % Κατεύθυνση καθόδου
   
    % Υπολογισμός νέου σημείου
    xk_bar=projection(xk + sk*dk);
    xk_new = xk + gk*(xk_bar-xk); 

    % Ενημέρωση του xk
    xk = xk_new;

    % Αποθήκευση της τρέχουσας τιμής της f
    f_values = [f_values, f(xk(1), xk(2))];

    % Αύξηση του μετρητή επαναλήψεων
    iter_cnt = iter_cnt + 1;
end

% Εμφάνιση αποτελεσμάτων
fprintf('Αρχικό σημείο: (%.2f, %.2f)\n', initial_point(1), initial_point(2));
fprintf('Τελικό σημείο: x* = (%.4f, %.4f)\n', xk(1), xk(2));
fprintf('Τελική τιμή: f(x*) = %.6f\n', f(xk(1), xk(2)));
fprintf('Συνολικές επαναλήψεις: %d\n', iter_cnt);

% Γράφημα σύγκλισης
figure;
plot(1:length(f_values), f_values, 'LineWidth', 2, 'Color', 'b');
title(sprintf('Σύγκλιση για το αρχικό σημείο (%.1f, %.1f)', initial_point(1), initial_point(2)));
xlabel('Αριθμός επαναλήψεων');
ylabel('f(x_k)');
grid on;