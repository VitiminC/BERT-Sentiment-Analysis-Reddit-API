create table original_full_table
(
    ID                     int auto_increment
        primary key,
    Title                  text     not null,
    Images                 text     not null,
    SubmissionCreatTime    datetime not null,
    SubmissionRetrieveTime datetime not null,
    Commenter              text     not null,
    Comment                text     not null,
    CommentCreatTime       datetime not null,
    CommentRetrieveTime    datetime not null,
    Status                 text     not null,
    Score                  int      not null,
    ControversialityScale  int      not null
);



create table submission_table
(
    SubmissionID           int auto_increment
        primary key,
    SubmissionTitle        text     not null,
    Images                 text     not null,
    SubmissionRetrieveTime datetime not null,
    SubmissionCreatTime    datetime not null,
    NumComments            int      null
);


create table comments_table
(
    SubmissionID          int      not null,
    CommentID             int      not null,
    Commenter             text     not null,
    Comment               text     not null,
    CommentCreatTime      datetime not null,
    CommentRetrieveTime   datetime not null,
    Status                text     not null,
    Score                 int      not null,
    ControversialityScale int      not null,
    constraint comments_table_full_table_ID_fk
        foreign key (SubmissionID) references full_table (ID)
            on update cascade on delete cascade
);


insert into comments_table
SELECT SubmissionID, ID, Commenter, Comment, CommentCreatTime, CommentRetrieveTime, Status, Score, ControversialityScale
FROM
    full_table, submission_table
where SubmissionTitle=Title;


-- add NumComments column
update full_table
inner join (select Title, count(Title) as Cnt from full_table
    group by Title
    having count(Title) >= 5) as table1
on full_table.Title=table1.Title
set full_table.NumComments=table1.Cnt;

drop table url_process_table;
create table url_process_table
(
    SubmissionID           int  not null,
    CommentID              int  not null,
    Uncleaned_Comment      text null,
    Embedded_Captions      text null,
    Stage1_Extracted       text null,
    Stage1_Cleaned_Comment text null,
    Stage2_Extracted       text null,
    Stage2_Cleaned_Comment text null,
    Stage3_Cleaned_Comment text null
);


create table emoji_extraction_table
(
	SubmissionID int not null,
	CommentID int not null,
	`Emoji/Emoticon` text null,
	Start_idx int null,
	Word_with_emoji text null,
	Comment text null
);


start transaction;
savepoint stage2;