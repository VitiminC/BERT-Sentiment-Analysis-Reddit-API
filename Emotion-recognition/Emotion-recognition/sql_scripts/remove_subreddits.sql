insert into subreddit_process_table
select SubmissionID, CommentID, Comment, extracted_subreddits, Updated_Comment, 'Incomplete sentence' as keep_or_discard
from (
         select SubmissionID,
                CommentID,
                Comment,
                regexp_substr(
                        Comment,
                        '(^[/\\s]?|[/\\s])[uUrR][/\\s][^\\s,.?!]*')     as extracted_subreddits,
                trim(regexp_replace(regexp_replace(
                                            Comment,
                                            '(^[/\\s]?|[/\\s])[uUrR][/\\s][^\\s,.?!]*',
                                            ''),
                                    '[[:space:]]+', ' ')) as Updated_Comment
         from stage1_comments_table
     ) as t1
where extracted_subreddits like BINARY '%/%'
and Updated_Comment not like '%.%.%'
and Updated_Comment like '%.'
union
select SubmissionID, CommentID, Comment, extracted_subreddits, Updated_Comment, 'Not a sentence' as keep_or_discard
from (
         select SubmissionID,
                CommentID,
                Comment,
                regexp_substr(
                        Comment,
                        '(^[/\\s]?|[/\\s])[uUrR][/\\s][^\\s,.?!]*')     as extracted_subreddits,
                trim(regexp_replace(regexp_replace(
                                            Comment,
                                            '(^[/\\s]?|[/\\s])[uUrR][/\\s][^\\s,.?!]*',
                                            ''),
                                    '[[:space:]]+', ' ')) as Updated_Comment
         from stage1_comments_table
     ) as t1
where extracted_subreddits like BINARY '%/%'
and Updated_Comment not like '%.%'
union
select SubmissionID, CommentID, Comment, extracted_subreddits, Updated_Comment, 'Multiple sentences' as keep_or_discard
from (
         select SubmissionID,
                CommentID,
                Comment,
                regexp_substr(
                        Comment,
                        '(^[/\\s]?|[/\\s])[uUrR][/\\s][^\\s,.?!]*')     as extracted_subreddits,
                trim(regexp_replace(regexp_replace(
                                            Comment,
                                            '(^[/\\s]?|[/\\s])[uUrR][/\\s][^\\s,.?!]*',
                                            ''),
                                    '[[:space:]]+', ' ')) as Updated_Comment
         from stage1_comments_table
     ) as t1
where extracted_subreddits like BINARY '%/%'
  and Updated_Comment like '%.%.%'
  and Updated_Comment not like '%..%'
  and Updated_Comment not like '%...%';