% ΘΕΜΑ 4 - ΜΕΘΟΔΟΣ ΤΗΣ ΔΙΧΟΤΟΜΟΥ ΜΕ ΧΡΗΣΗ ΠΑΡΑΓΩΓΟΥ (Αλγόριθμος 5.1.4)
clear 
close all
clc


% Συνάρτηση για την υλοποίηση της μεθόδου Διχοτόμου με χρήση παραγώγου
% που επιστρέφει το τελικό διάστημα, τον αριθμό των υπολογισμών και τον αριθμό υπολογισμών της f(x)
function [num_of_iterations, f_calculations, intervals] = bisectionMethodWithDerivative(f, df, a, b, l)
    % Προκαθορισμός μεγέθους πίνακα διαστημάτων
    max_iterations = ceil(log2((b - a) / l)); % Υπολογισμός μέγιστου αριθμού επαναλήψεων
    intervals = zeros(max_iterations + 1, 2); % +1 για το αρχικό διάστημα
    intervals(1, :) = [a, b]; % Αρχικοποίηση με το αρχικό διάστημα
    num_of_iterations = 0;
    f_calculations = 0;

    % Επαναληπτική διαδικασία διχοτόμησης
    iteration_cnt = 1; % Μετρητής επαναλήψεων
    while (b - a) > l
        % Υπολογισμός του μεσαίου σημείου
        c = (a + b) / 2;
        f_c = f(c); % Υπολογισμός της συνάρτησης
        f_calculations = f_calculations + 1; % Μέτρηση της συνάρτησης
        df_c = df(c);
        num_of_iterations = num_of_iterations + 1;

        % Ανανέωση του διαστήματος ανάλογα με την τιμή της παραγώγου στο c
        if df_c == 0
            a = c;
            b = c;
        elseif df_c > 0
            b = c;
        else
            a = c;
        end

        % Αποθήκευση των τρέχουσων τιμών των a και b στον πίνακα intervals
        iteration_cnt = iteration_cnt + 1; % Αύξηση του μετρητή επαναλήψεων
        intervals(iteration_cnt, :) = [a, b];
    end
    intervals = intervals(1:iteration_cnt, :); % Αποκοπή του πίνακα στο πραγματικό μέγεθος
end


% ΕΡΩΤΗΜΑΤΑ
% Ορισμός των συναρτήσεων και των παραγώγων τους
f = {@(x) (x - 2)^2 + x * log(x + 3), ...
     @(x) exp(-2 * x) + (x - 2)^2, ...
     @(x) exp(x) * (x^3 - 1) + (x - 1) * sin(x)};
df = {@(x) 2 * (x - 2) + log(x + 3) + x / (x + 3), ...
      @(x) -2 * exp(-2 * x) + 2 * (x - 2), ...
      @(x) exp(x) * (x^3 + 3 * x^2 - 1) + (x - 1) * cos(x) + sin(x)};

% Αρχικό διάστημα αναζήτησης [a b] και οι παράμετροι l
a = -1;
b = 3;
l_values = 0.0021:0.00025:0.0106; % Τελικό εύρος αναζήτησης

% Δέσμευση μνήμης για την αποθήκευση των υπολογισμών
f_calculations_all_f = zeros(3, length(l_values)); % Προκαθορισμός πίνακα για f(x) υπολογισμούς
intervals_all_f = cell(3, length(l_values)); % Δεδομένα για τα διαστήματα

% Εφαρμογή της μεθόδου Διχοτόμου με χρήση παραγώγου
for funcIdx = 1:3
    % Εφαρμογή της μεθόδου Διχοτόμου για κάθε τιμή του l
    for i = 1:length(l_values)
        l = l_values(i);
        [~, f_calculations, intervals] = bisectionMethodWithDerivative(f{funcIdx}, df{funcIdx}, a, b, l);
        f_calculations_all_f(funcIdx, i) = f_calculations; % Αποθήκευση υπολογισμών f(x)
        intervals_all_f{funcIdx, i} = intervals; % Αποθήκευση διαστημάτων
    end
    
    % Σχεδίαση γραφημάτων για τα διαστήματα
    figure;
    hold on;
    for i = 1:length(l_values)
        if size(intervals_all_f{funcIdx, i}, 1) >= 1 % Έλεγχος για ύπαρξη διαστήματος
            k = 1:size(intervals_all_f{funcIdx, i}, 1); % Αριθμός επαναλήψεων
            plot(k, intervals_all_f{funcIdx, i}(:, 1), '-o', 'DisplayName', ['a, l = ', num2str(l_values(i))]);
            plot(k, intervals_all_f{funcIdx, i}(:, 2), '-x', 'DisplayName', ['b, l = ', num2str(l_values(i))]);
        end
    end
    title(['Συνάρτηση f', num2str(funcIdx)]);
    xlabel('Επανάληψη (k)');
    ylabel('Διάστημα [a_k, b_k]');
    hold off;

    % Σχεδίαση γραφήματος υπολογισμών f(x)
    figure;
    plot(l_values, f_calculations_all_f(funcIdx, :), '-o', 'MarkerFaceColor',[1 0 0]);
    title(['Συνάρτηση f', num2str(funcIdx)]);
    xlabel('Τελικό εύρος (l)');
    ylabel('Αριθμός υπολογισμών της f');
end
