import * as React from 'react';
import { useEffect, useState } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, Box, Button, Grid } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import SessionList from './SessionList';
import { getCourses, Course, createCourse } from '../../api/dashboard';
import NewCourseModal from './NewCourseModal';

export default function CourseList() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [open, setOpen] = React.useState(false);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        if (token) {
          const courses = await getCourses(token);
          setCourses(courses);
        }
      } catch (error) {
        console.error('Failed to fetch courses:', error);
      }
    };

    fetchCourses();
  }, []);

  const handleCloseModal = () => setOpen(false);

  const handleSaveCourse = async (course: { name: string; date: string; description: string }) => {
    try {
      const token = localStorage.getItem('token') || sessionStorage.getItem('token');
      if (token) {
        // Call API to create a new course
        const newCourse = await createCourse(token, course);

        // Update the state with the newly created course
        setCourses((prevCourses) => [...prevCourses, newCourse]);
      }
    } catch (error) {
      console.error('Failed to save course:', error);
    } finally {
      setOpen(false); // Close the modal after saving the course
    }
  };

  return (
    <React.Fragment>
      {courses.map((course) => (
        <Accordion key={course.id} defaultExpanded>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls={`panel${course.id}-content`}
            id={`panel${course.id}-header`}
          >
            <Typography variant="h6">{course.name}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body1" gutterBottom>
                {new Date(course.date).toLocaleDateString()}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {course.description}
              </Typography>
            </Box>
            <SessionList
              course={course.id}
            />
          </AccordionDetails>
        </Accordion>
      ))}
      <Grid container justifyContent="flex-end" sx={{ mt: 3 }}>
        <Button variant="contained" color="primary" onClick={() => setOpen(true)}>
          New Course
        </Button>
      </Grid>
      <NewCourseModal open={open} onClose={handleCloseModal} onSave={handleSaveCourse} />
    </React.Fragment>
  );
}
