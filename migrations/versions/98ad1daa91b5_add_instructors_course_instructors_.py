from alembic import op
import sqlalchemy as sa

revision = '0001_add_instructors_and_submissions'
down_revision = None  # or your last revision id if you already use Alembic

def upgrade():
    op.create_table(
        'instructors',
        sa.Column('instructor_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id'), unique=True),
        sa.Column('teacher_id', sa.Integer, sa.ForeignKey('teachers.teacher_id')),
        sa.Column('fname', sa.String(100)),
        sa.Column('mname', sa.String(100)),
        sa.Column('lname', sa.String(100)),
        sa.Column('contact_no', sa.String(100)),
        sa.Column('address_line1', sa.String(100)),
        sa.Column('address_line2', sa.String(100)),
        sa.Column('address_line3', sa.String(100)),
        sa.Column('status', sa.String, server_default='active'),
        sa.Column('created_at', sa.DateTime),
    )
    op.create_table(
        'course_instructors',
        sa.Column('course_instructor_id', sa.Integer, primary_key=True),
        sa.Column('instructor_id', sa.Integer, sa.ForeignKey('instructors.instructor_id', ondelete="CASCADE")),
        sa.Column('course_id', sa.Integer, sa.ForeignKey('courses.course_id', ondelete="CASCADE")),
        sa.Column('can_upload_assessment', sa.Boolean, server_default=sa.text('false')),
        sa.Column('can_grade', sa.Boolean, server_default=sa.text('false')),
        sa.UniqueConstraint('instructor_id', 'course_id', name='uq_instructor_course')
    )
    op.create_table(
        'assessment_files',
        sa.Column('assessment_file_id', sa.Integer, primary_key=True),
        sa.Column('assessment_id', sa.Integer, sa.ForeignKey('assessments.assessment_id', ondelete="CASCADE")),
        sa.Column('file_path', sa.Text, nullable=False),
        sa.Column('original_filename', sa.Text),
        sa.Column('uploaded_at', sa.DateTime),
        sa.Column('file_type', sa.String(20))
    )
    op.create_table(
        'student_submissions',
        sa.Column('submission_id', sa.Integer, primary_key=True),
        sa.Column('assessment_id', sa.Integer, sa.ForeignKey('assessments.assessment_id', ondelete="CASCADE")),
        sa.Column('student_id', sa.Integer, sa.ForeignKey('students.student_id', ondelete="CASCADE")),
        sa.Column('file_path', sa.Text, nullable=False),
        sa.Column('original_filename', sa.Text),
        sa.Column('uploaded_at', sa.DateTime),
        sa.Column('status', sa.String(20), server_default='submitted'),
        sa.Column('notes', sa.Text)
    )
    op.add_column('assessment_results', sa.Column('submission_id', sa.Integer, sa.ForeignKey('student_submissions.submission_id'), nullable=True))
    op.add_column('assessment_results', sa.Column('feedback', sa.Text, nullable=True))

def downgrade():
    op.drop_column('assessment_results', 'feedback')
    op.drop_column('assessment_results', 'submission_id')
    op.drop_table('student_submissions')
    op.drop_table('assessment_files')
    op.drop_table('course_instructors')
    op.drop_table('instructors')
