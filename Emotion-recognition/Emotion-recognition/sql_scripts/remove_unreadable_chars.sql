-- remove &gt;, &lt;, &amp;, &nbsp;

select SubmissionTitle,
       trim(regexp_replace(regexp_replace(SubmissionTitle, '&gt;|&lt;|&amp;|&nbsp;', ''), '[[:space:]]+', ' '))
from original_submission_table
where SubmissionTitle like '%&gt;%'
or SubmissionTitle like '%&lt;%'
or SubmissionTitle like '%&amp;%'
or SubmissionTitle like '%&nbsp;%';


update original_submission_table
set SubmissionTitle = trim(regexp_replace(regexp_replace(SubmissionTitle, '&gt;|&lt;|&amp;|&nbsp;', ''), '[[:space:]]+', ' '))
where SubmissionTitle like '%&gt;%'
or SubmissionTitle like '%&lt;%'
or SubmissionTitle like '%&amp;%'
or SubmissionTitle like '%&nbsp;%';


-- replace “” ‘’ with "", ''

update stage1_comments_table
set Comment = replace(
                replace(
                    replace(
                        replace(Comment, '“', '"'),
                        '”', '"'),
                    '‘', '\''),
                '’', '\'')
where Comment like '%“%'
   or Comment like '%”%'
   or Comment like '%‘%'
   or Comment like '%’%';


-- remove failed submission alerts

delete
from stage1_comments_table
where Comment like '%your comment was removed for%'
or Comment like '%thank you for your submission%'
or Comment like '%I am a bot and this action was performed automatically%'
or Comment like '%[removed]%'
or Comment like '%[deleted]%'
or Comment like '%Desktop link%'
or Comment like '%^I ^am ^a ^bot ^providing ^a ^(bad) ^service%'
or Comment like '%Reddit Cliches have been observed by%'
or Comment like '%Thank you for your participation%'
or Comment like '%a bot, *bleep*, *bloop*.%'


delete
from stage1_comments_table
where ord(Comment) > 500
and CommentID not in (select CommentID from emoji_extraction_table)
order by ord(Comment) asc;


update stage1_comments_table
set Comment = trim(regexp_replace(replace(Comment, '#x200B;', ''), '[[:space:]]+', ' '))
where Comment like '%#x200B;%';


select *
from stage1_comments_table
where Comment like '%/r/ comnts%';


truncate table processed_comments_detail;