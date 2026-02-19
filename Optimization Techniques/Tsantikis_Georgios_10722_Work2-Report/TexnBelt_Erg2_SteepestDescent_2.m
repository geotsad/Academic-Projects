% ΘΕΜΑ 2 - ΜΕΘΟΔΟΣ ΜΕΓΙΣΤΗΣ ΚΑΘΟΔΟΥ (Αλγόριθμος 5.2.1)
clc; clearvars; close all;

% Συνάρτηση f
f = @(x, y) x^5 * exp(-x^2 - y^2);

% Gradient της f
grad_f = @(x, y) [5*x^4*exp(-x^2 - y^2) - 2*x^6*exp(-x^2 - y^2), ...
                  -2*x^5*y*exp(-x^2 - y^2)];

initial_points = [0, 0; -1, 1; 1, -1]; % Αρχικά σημεία
gk_fixed = 0.3; % Σταθερό γκ της επιλογής μου
epsilon = 0.01; % Κριτήριο τερματισμού

% Αποθήκευση αποτελεσμάτων για τα plots
all_results = cell(size(initial_points, 1), 3);

% Υπολογισμοί
for i = 1:size(initial_points, 1)
    x0 = initial_points(i, :);
    for step = 1:3
        xk = x0;
        iter_cnt = 1;
        f_values = []; % Αποθήκευση τιμών της f για το plot σύγκλισης
        
        while norm(grad_f(xk(1), xk(2))) >= epsilon 
            % Αποθήκευση τιμής f(x_k)
            f_values = [f_values, f(xk(1), xk(2))];

            gradf = grad_f(xk(1), xk(2));
            dk = -gradf ; % Κατεύθυνση καθόδου

             %2ο ΚΡΙΤΗΡΙΟ ΚΑΛΗΣ ΛΕΙΤΟΥΡΓΙΑΣ
            if dk' * gradf >=0  
                fprintf(['Το 2ο κριτήριο καλής λειτουργίας στην %d επανάληψη δεν ικανοποιείται για το ' ...
                         'αρχικο σημείο (%.2f, %.2f).\n'],iter_cnt, initial_points(i, 1), initial_points(i, 2));
                break;
            end
            
            % Επιλογή βήματος
            switch step
                case 1 % Σταθερό βήμα
                    gk = gk_fixed;
                case 2 % Βήμα που ελαχιστοποιεί την f με κανόνα διχοτόμου
                    a = 0; b = 1; % Αρχικό διάστημα
                    e = 0.001;
                    lambda = e*10; % Μικρή απόσταση
                    while (b - a) > lambda
                        gk1 = (a + b) / 2 - e;
                        gk2 = (a + b) / 2 + e;
                        f1 = f(xk(1) + gk1*dk(1), xk(2) + gk1*dk(2));
                        f2 = f(xk(1) + gk2*dk(1), xk(2) + gk2*dk(2));
                        if f1 < f2
                            b = gk2;
                        else
                            a = gk1;
                        end
                    end
                    gk = (a + b) / 2; % Το βέλτιστο γκ
                case 3 % Βήμα με τον κανόνα Armijo
                    s = 1;
                    beta = 0.4; % ε [0.1, 0.5]
                    alpha = 0.01; % ε [1e-5, 1e-1]
                    m=0;
                    gk=s;
                    while f(xk(1) + gk*dk(1), xk(2) + gk*dk(2)) > ...
                          f(xk(1), xk(2)) + alpha*gk*(gradf*dk')
                        m=m+1;
                        gk = s*beta^m;
                    end
            end
            
            % Ενημέρωση σημείου
            xk_new = xk + gk * dk;
            
            % 1ο ΚΡΙΤΗΡΙΟ ΚΑΛΗΣ ΛΕΙΤΟΥΡΓΙΑΣ
            if f(xk_new(1), xk_new(2)) >= f(xk(1), xk(2))
                fprintf(['Το 1ο κριτήριο καλής λειτουργίας στην %d επανάληψη δεν ικανοποιείται για το ' ...
                         'αρχικό σημείο (%.2f, %.2f).\n'], iter_cnt, initial_points(i, 1), initial_points(i, 2));
                break;
            end

            % Ενημέρωση για την επόμενη επανάληψη
            xk = xk_new;
            iter_cnt = iter_cnt + 1;      
        end
        
        % Αποθήκευση αποτελεσμάτων
        all_results{i, step} = struct('x', xk, 'f_val', f(xk(1), xk(2)), ...
                                           'iterations', iter_cnt, 'f_values', f_values);
                                           
        % Δημιουργία ξεχωριστού γραφήματος για κάθε περίπτωση
        figure;
        plot(1:iter_cnt-1, f_values, 'LineWidth', 2);
        title(sprintf('Σύγκλιση για (%d,%d), Περίπτωση %d', x0(1), x0(2), step));
        xlabel('Αριθμός επαναλήψεων');
        ylabel('f(x_k)');
        grid on;
    end
end

% Εμφάνιση αποτελεσμάτων
for i = 1:size(initial_points, 1)
    fprintf('Αρχικό σημείο: (%.2f, %.2f)\n', initial_points(i, 1), initial_points(i, 2));
    for step = 1:3
        res = all_results{i, step};
        fprintf('  Περίπτωση %d: x* = (%.4f, %.4f), f(x*) = %.6f, Επαναλήψεις = %d\n', ...
                step, res.x(1), res.x(2), res.f_val, res.iterations-1);
    end
end