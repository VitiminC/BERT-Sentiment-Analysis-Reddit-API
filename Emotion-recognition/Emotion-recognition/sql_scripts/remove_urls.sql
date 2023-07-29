select SubmissionID,
       CommentID,
       Uncleaned_Comment,
       Embedded_Captions,
       Stage1_Extracted,
       Stage1_Cleaned_Comment,
       SUBSTRING_INDEX(
               regexp_substr(
                       Stage2_Cleaned_Comment,
                       '(https?:\/\/(?:www\.|(?!www|WAP))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www|WAP\.|(?!www|WAP))[a-zA-Z0-9]+\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9]+\.[^\s]{2,}).*'),
               ' ', 1)                 as Stage2_Extracted,
       Stage2_Cleaned_Comment,
       if(
               LOCATE('http', Stage2_Cleaned_Comment) > 0,
               replace(
                       Stage2_Cleaned_Comment,
                       SUBSTRING_INDEX(
                               regexp_substr(
                                       Stage2_Cleaned_Comment,
                                       '(https?:\/\/(?:www\.|(?!www|WAP))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www|WAP\.|(?!www|WAP))[a-zA-Z0-9]+\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9]+\.[^\s]{2,}).*'),
                               ' ', 1),
                       ''),
               Stage2_Cleaned_Comment) as Stage3_Cleaned_Comment

from (
         select SubmissionID,
                CommentID,
                Uncleaned_Comment,
                Extracted                    as Stage1_Extracted,
                Comment_removed_embedded_url as Stage1_Cleaned_Comment,
                if(LOCATE('http', Cleaned_Comment) > 0, replace(Cleaned_Comment, Extracted, ''),
                   Cleaned_Comment)          as Stage2_Cleaned_Comment,
                Embedded_Captions
         from (
                  select SubmissionID,
                         CommentID,
                         Comment                                                      as Uncleaned_Comment,
                         Extracted,
                         Comment_removed_embedded_url,
                         regexp_replace(Comment_removed_all_url, '[[:space:]]+', ' ') as Cleaned_Comment,
                         if(extract_caption = 0, 'False', 'True')                     as 'Embedded_Captions'
                  from (
                           select SubmissionID,
                                  CommentID,
                                  Comment,
                                  SUBSTRING_INDEX(
                                          regexp_substr(
                                                  Comment_removed_embedded_url,
                                                  '(https?:\/\/(?:www\.|(?!www|WAP))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www|WAP\.|(?!www|WAP))[a-zA-Z0-9]+\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9]+\.[^\s]{2,}).*'),
                                          ' ', 1)                        as Extracted,
                                  Comment_removed_embedded_url,
                                  extract_caption,
                                  if(extract_caption = 0,
                                     trim(replace(
                                             Comment_removed_embedded_url,
                                             SUBSTRING_INDEX(
                                                     regexp_substr(
                                                             Comment_removed_embedded_url,
                                                             '(https?:\/\/(?:www\.|(?!www|WAP))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www|WAP\.|(?!www|WAP))[a-zA-Z0-9]+\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9]+\.[^\s]{2,}).*'),
                                                     ' ', 1),
                                             '')),
                                     trim(Comment_removed_embedded_url)) as Comment_removed_all_url
                           from (
                                    select *
                                    from (
                                             select SubmissionID,
                                                    CommentID,
                                                    Comment,
                                                    Comment_removed_embedded_url,
                                                    strcmp(Comment, Comment_removed_embedded_url) as extract_caption
                                             from (
                                                      select SubmissionID,
                                                             CommentID,
                                                             Comment,
                                                             regexp_replace(regexp_replace(
                                                                                    Comment,
                                                                                    '[\\(\\[](https?:\/\/(?:www\.|(?!www|WAP))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www|WAP\.|(?!www|WAP))[a-zA-Z0-9]+\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9]+\.[^\s]{2,}).*[\\)\\]]',
                                                                                    ''),
                                                                            '\\[|\\]',
                                                                            '') as Comment_removed_embedded_url
                                                      from original_comments_table
                                                      where Comment like '%http%'
                                                         or Comment like '%http%www.%'
                                                         or Comment like '%.com%'
                                                  ) as comment_removed_embedded_url_table1
                                         ) as comment_removed_embedded_url_table2
                                ) as comment_removed_all_url_table3
                       ) as comment_removed_all_url_table4

                  where length(Comment_removed_all_url) > 0
                    and Comment_removed_all_url is not null
              ) as further_processed_table
     ) as final_table;


