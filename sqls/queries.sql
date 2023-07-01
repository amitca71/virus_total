with t_rank_by_dep as (select  first_name, last_name, department_id,  salary, RANK() OVER (PARTITION BY department_id ORDER BY salary desc) AS sal_rank from employees ),
     t_sal_gaps as(SELECT first_name, last_name, department_id,  salary, sal_rank, salary-lag(salary, -1) OVER (PARTITION BY department_id ORDER BY salary desc ) as salary_gap from t_rank_by_dep),
     t_first_ranks as (select * from t_sal_gaps where sal_rank=1),
     t_dept as (select department_id, department_name from departments)
     select first_name, last_name, department_name,  salary, salary_gap from t_first_ranks
     left join t_dept on t_dept.department_id=t_first_ranks.department_id


with t_traffic_and_promotions as (select site_visitors.site, visit_date,number_of_visitors, start_date, end_date from site_visitors left join promotion_dates on site_visitors.site=promotion_dates.site),
t_promotion_traffic_sum as (select site, sum(number_of_visitors) sum_prom_num_visitors from t_traffic_and_promotions where visit_date between start_date and end_date group by site),
t_all_traffic_sum as (select site, sum (number_of_visitors) sum_total_num_visitors from site_visitors group by site)
select t_all_traffic_sum.site, nvl(sum_prom_num_visitors,0)/sum_total_num_visitors as promotion_traffic_ratio from t_all_traffic_sum 
left join t_promotion_traffic_sum on t_all_traffic_sum.site=t_promotion_traffic_sum.site
