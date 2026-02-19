% ΘΕΜΑ 3 - ΜΕΘΟΔΟΣ FIBONACCI (Αλγόριθμος 5.1.3)
clear 
close all
clc

% Συνάρτηση για την υλοποίηση της μεθόδου Fibonacci που επιστρέφει 
% το τελικό διάστημα και τον αριθμό των υπολογισμών
function [num_of_calculations, a_values, b_values] = fibonacciMethod(f, a, b, l)
    % Υπολογισμός του απαιτούμενου αριθμού επαναλήψεων (n) εκ των προτέρων
    % ώστε να ικανοποιείται η σχέση (1/Fn)*(b1-a1) < l
    L = b - a;
    n = 1;
    while fibonacci(n) <= L / l
        n = n + 1;
    end

    % Αρχικοποίηση των μεταβλητών
    k = 1;
    F_n = fibonacci(n);
    F_n_minus_1 = fibonacci(n - 1);
    F_n_minus_2 = fibonacci(n - 2);
   
    % Αρχικοποίηση των πινάκων για αποθήκευση των τιμών των διαστημάτων
    a_values = zeros(1, n);
    b_values = zeros(1, n);
    
    % Αποθήκευση των αρχικών τιμών των a, b
    a_values(k) = a;
    b_values(k) = b;

    % Αρχικά εσωτερικά σημεία
    x1 = a + (F_n_minus_2 / F_n) * (b - a);
    x2 = a + (F_n_minus_1 / F_n) * (b - a);
    f_x1 = f(x1);
    f_x2 = f(x2);
    num_of_calculations = 2; % Αρχικοί υπολογισμοί της συνάρτησης

    % Επαναληπτική διαδικασία εύρεσης των νέων διαστημάτων
     while k <= n - 2
        if f_x1 > f_x2
            % Ανανέωση διαστήματος σε [x1, b]
            a = x1;
            x1 = x2;
            f_x1 = f_x2;
            F_n = F_n_minus_1;
            F_n_minus_1 = F_n_minus_2;
            F_n_minus_2 = F_n - F_n_minus_1;
            x2 = a + (F_n_minus_1 / F_n) * (b - a);
            f_x2 = f(x2);
            num_of_calculations = num_of_calculations + 1;
        else
            % Ανανέωση διαστήματος σε [a, x2]
            b = x2;
            x2 = x1;
            f_x2 = f_x1;
            F_n = F_n_minus_1;
            F_n_minus_1 = F_n_minus_2;
            F_n_minus_2 = F_n - F_n_minus_1;
            x1 = a + (F_n_minus_2 / F_n) * (b - a);
            f_x1 = f(x1);
            num_of_calculations = num_of_calculations + 1;
        end
        k = k + 1;

        % Αποθήκευση των τρέχουσων τιμών των a, b
        a_values(k) = a;
        b_values(k) = b;
    end

    % Στην τελευταία επανάληψη συμπίπτουν τα x1, x2 οπότε προσθέτω τη
    % σταθερά ε για να υπολογίσω και το δεύτερο σημείο
    epsilon = l/10; % Αυθαίρετα μικρή, συνήθως l/10
    x2 = x1 + epsilon;
    if f(x1) > f(x2)
        a = x1;
    else
        b = x2;
    end
        
    % Αποθήκευση των τελικών τιμών των a, b
    a_values(k+1) = a;
    b_values(k+1) = b;
end


% ΕΡΩΤΗΜΑΤΑ
% Οι αντικειμενικές συναρτήσεις για την εφαρμογή της παραπάνω μεθόδου
f1 = @(x) (x-2)^2 + x*log(x+3);
f2 = @(x) exp(-2*x) + (x-2)^2;
f3 = @(x) exp(x)*(x^3-1) + (x-1)*sin(x);

% Αρχικό διάστημα αναζήτησης [a b] και οι παράμετροι l, ε
a = -1;
b = 3;
epsilon = 0.001;
l_values = 0.0021:0.00025:0.0106; % Τελικό εύρος αναζήτησης

% Δέσμευση μνήμης για την αποθήκευση των τιμών a, b για τη σχεδίαση
a_values_f1 = cell(1, length(l_values));
b_values_f1 = cell(1, length(l_values));
a_values_f2 = cell(1, length(l_values));
b_values_f2 = cell(1, length(l_values));
a_values_f3 = cell(1, length(l_values));
b_values_f3 = cell(1, length(l_values));

% Εφαρμογή της μεθόδου Fibonacci για κάθε 
% συνάρτηση και διάφορες τιμές του l
for i = 1:length(l_values)
    l = l_values(i);
    [~, a_values_f1{i}, b_values_f1{i}] = fibonacciMethod(f1, a, b, l);
    [~, a_values_f2{i}, b_values_f2{i}] = fibonacciMethod(f2, a, b, l);
    [~, a_values_f3{i}, b_values_f3{i}] = fibonacciMethod(f3, a, b, l);
end

% Σχεδίαση για το γράφημα της συνάρτησης f1
figure;
hold on;
for i = 1:length(l_values)
    k = 1:length(a_values_f1{i}); % Number of iterations
    plot(k, a_values_f1{i}, '-o', 'DisplayName', ['a, l = ', num2str(l_values(i))]);
    plot(k, b_values_f1{i}, '-x', 'DisplayName', ['b, l = ', num2str(l_values(i))]);
end
title('Συνάρτηση f1');
xlabel('Επανάληψη (k)');
ylabel('Διάστημα [a_k, b_k]');
hold off;

% Σχεδίαση για το γράφημα της συνάρτησης f2
figure;
hold on;
for i = 1:length(l_values)
    k = 1:length(a_values_f2{i}); % Number of iterations
    plot(k, a_values_f2{i}, '-o', 'DisplayName', ['a, tol = ', num2str(l_values(i))]);
    plot(k, b_values_f2{i}, '-x', 'DisplayName', ['b, tol = ', num2str(l_values(i))]);
end
title('Συνάρτηση f2');
xlabel('Επανάληψη (k)');
ylabel('Διάστημα [a_k, b_k]');
hold off;

% Σχεδίαση για το γράφημα της συνάρτησης f3
figure;
hold on;
for i = 1:length(l_values)
    k = 1:length(a_values_f3{i}); % Number of iterations
    plot(k, a_values_f3{i}, '-o', 'DisplayName', ['a, tol = ', num2str(l_values(i))]);
    plot(k, b_values_f3{i}, '-x', 'DisplayName', ['b, tol = ', num2str(l_values(i))]);
end
title('Συνάρτηση f3');
xlabel('Επανάληψη (k)');
ylabel('Διάστημα [a_k, b_k]');
hold off;


%%%%%
eval_counts_f1 = zeros(size(l_values));
eval_counts_f2 = zeros(size(l_values));
eval_counts_f3 = zeros(size(l_values));

% Run Fibonacci search for each function and tolerance level
for i = 1:length(l_values)
    l = l_values(i);
    [eval_counts_f1(i)] = fibonacciMethod(f1, a, b, l);
    [eval_counts_f2(i)] = fibonacciMethod(f2, a, b, l);
    [eval_counts_f3(i)] = fibonacciMethod(f3, a, b, l);
end

% Σχεδίαση για την f1
figure;
plot(l_values, eval_counts_f1, '-o', 'MarkerFaceColor',[1 0 0]);
title('Συνάρτηση f1');
xlabel('Τελικό εύρος (l)');
ylabel('Αριθμός υπολογισμών της f');

% Σχεδίαση για την f2
figure;
plot(l_values, eval_counts_f2, '-o', 'MarkerFaceColor',[1 0 0]);
title('Συνάρτηση f2');
xlabel('Τελικό εύρος (l)');
ylabel('Αριθμός υπολογισμών της f');

% Σχεδίαση για την f3
figure;
plot(l_values, eval_counts_f3, '-o', 'MarkerFaceColor',[1 0 0]);
title('Συνάρτηση f3');
xlabel('Τελικό εύρος (l)');
ylabel('Αριθμός υπολογισμών της f');