-- check out the duplicate submissions and the corresponding comments
select *
from original_comments_table
where find_in_set(SubmissionID,
(select submissionid_lst
       from (
                select GROUP_CONCAT(distinct SubmissionID SEPARATOR ',') as submissionid_lst,
                       SubmissionTitle,
                       count(SubmissionTitle)
                from original_submission_table
                group by SubmissionTitle
                having count(SubmissionTitle) > 1
                limit 1
            ) as table1
      )
    ) <> 0;



-- 1888 duplicated submissions
select SubmissionTitle, GROUP_CONCAT(distinct SubmissionID SEPARATOR ', ') from  submission_table_with_deplicates
group by SubmissionTitle
having count(SubmissionTitle) > 1
order by count(SubmissionTitle) desc;



-- delete all duplicates, keep one among each duplicated group
delete A
from
    submission_table as A,
    submission_table as B
where A.SubmissionID < B.SubmissionID
and A.SubmissionTitle <=> B.SubmissionTitle;


-- check no duplicates left
select submissionid_lst
       from (
                select GROUP_CONCAT(distinct SubmissionID SEPARATOR ',') as submissionid_lst,
                       count(SubmissionTitle)
                from submission_table
                group by SubmissionTitle
                having count(SubmissionTitle) > 1
            ) as table1;

