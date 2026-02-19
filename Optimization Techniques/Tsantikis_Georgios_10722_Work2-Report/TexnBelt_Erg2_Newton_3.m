% ΘΕΜΑ 3 - ΜΕΘΟΔΟΣ NEWTON (Αλγόριθμος 5.2.2)
clc; clearvars; close all;

% Συνάρτηση f
f = @(x, y) x^5 * exp(-x^2 - y^2);

% Gradient της f
grad_f = @(x, y) [5*x^4*exp(-x^2 - y^2) - 2*x^6*exp(-x^2 - y^2), ...
                  -2*x^5*y*exp(-x^2 - y^2)];

% Hessian της f
hessian_f = @(x, y) [
    20*x^3*exp(-x^2 - y^2) - 22*x^5*exp(-x^2 - y^2) + 4*x^7*exp(-x^2 - y^2), ...
    2*x^4*(2*x^2-5)*y*exp(-x^2 - y^2);
    2*x^4*(2*x^2-5)*y*exp(-x^2 - y^2), ...
    -2*x^5*exp(-x^2 - y^2) + 4*x^5*y^2*exp(-x^2 - y^2)
];

initial_points = [0, 0; -1, 1; 1, -1]; % Αρχικά σημεία
gk_fixed = 0.2; % Σταθερό γκ της επιλογής μου
epsilon = 0.01; % Κριτήριο τερματισμού
HisPositive = true;
max_iter = 1200; % Μέγιστος αριθμός επαναλήψεων

% Αποθήκευση αποτελεσμάτων για τα plots
all_results = cell(size(initial_points, 1), 3);

% Υπολογισμοί
for i = 1:size(initial_points, 1)
    x0 = initial_points(i, :);
    for step = 1:3
        xk = x0;
        iter_cnt = 1;
        f_values = []; % Αποθήκευση τιμών της f για το plot σύγκλισης
        
        while norm(grad_f(xk(1), xk(2))) >= epsilon && iter_cnt < max_iter
            % Αποθήκευση τιμής f(x_k)
            f_values = [f_values, f(xk(1), xk(2))];

            gradf = grad_f(xk(1), xk(2));
            H = hessian_f(xk(1), xk(2));

            % Έλεγχος θετικής οριστικότητας για αδυναμία εκτέλεσης του μεθόδου Newton
            if all(eig(H) > 0) 
                % Υπολογισμός της κατεύθυνσης Newton
                dk = -inv(H) * gradf'; % Σημείωση: dk είναι διάνυσμα στήλης

    
                % Επιλογή βήματος
                switch step
                    case 1 % Σταθερό βήμα
                        gk = gk_fixed;
                    case 2 % Βήμα που ελαχιστοποιεί την f με κανόνα διχοτόμου
                        a = 0; b = 1; % Αρχικό διάστημα
                        e=0.001;
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
                        beta = 0.5; % ε [0.1, 0.5]
                        alpha = 0.01; % ε [1e-5, 1e-1]
                        m=0;
                        gk=s;
                        while f(xk(1) + gk*dk(1), xk(2) + gk*dk(2)) > ...
                              f(xk(1), xk(2)) + alpha*gk*(gradf*dk)
                            m=m+1;
                            gk = s*beta^m;
                        end
                end
                
                % Ενημέρωση σημείου
                xk_new = xk + gk * dk;
                
              
                % Ενημέρωση για την επόμενη επανάληψη
                xk = xk_new;
                iter_cnt = iter_cnt + 1;
            else
                HisPositive = false; 
                fprintf(['Ο εσσιανός δεν είναι θετικά ορισμένος στην %d επανάληψη για το ' ...
                         'αρχικό σημείο (%.2f, %.2f).\n'], iter_cnt, initial_points(i, 1), initial_points(i, 2));
               break;
            end
        end
        
        if all(eig(hessian_f(xk(1), xk(2)))>0)  
            % Αποθήκευση αποτελεσμάτων
            all_results{i, step} = struct('x', xk, 'f_val', f(xk(1), xk(2)), ...
                                               'iterations', iter_cnt, 'f_values', f_values);
                                    
            % Δημιουργία γραφήματος
            figure;
            plot(1:iter_cnt-1, f_values, 'LineWidth', 2);
            title(sprintf('Σύγκλιση για (%d,%d), Μέθοδος Newton', initial_points(i, 1), initial_points(i, 2)));
            xlabel('Αριθμός επαναλήψεων');
            ylabel('f(x_k)');
            grid on;
        else
            break;
        end
    end
end


if HisPositive
    % Εμφάνιση αποτελεσμάτων
    for i = 1:size(initial_points, 1)
        fprintf('Αρχικό σημείο: (%.2f, %.2f)\n', initial_points(i, 1), initial_points(i, 2));
        for step = 1:3
            res = all_results{i, step};
            fprintf('  Περίπτωση %d: x* = (%.4f, %.4f), f(x*) = %.6f, Επαναλήψεις = %d\n', ...
                    step, res.x(1), res.x(2), res.f_val, res.iterations-1);
        end
    end
end