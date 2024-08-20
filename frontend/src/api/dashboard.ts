import axios, { AxiosResponse } from 'axios';

export interface Course {
    id: number;
    name: string;
    date: string;
    description: string;
    reflectometers: Reflectometer[];
}

export interface Reflectometer {
    id: number;
    date: string;
    name: string;
    url: string;
    responses: number;
    curveData: DataPoint[];
    keyMoments: KeyMoment[];
}

export interface DataPoint {
    x: number;
    y: number;
}

export interface KeyMoment extends DataPoint {
    details: {
        whatHappened: string;
        whenHappened: string;
        thoughts: string;
        feelings: string;
        actionsTaken: string;
        consequences: string;
    };
}

// Fetch all courses
export const getCourses = async (token: string): Promise<Course[]> => {
    const response: AxiosResponse<Course[]> = await axios.get('/api/courses', {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

// Create a new course
export const createCourse = async (
    token: string,
    course: { name: string; date: string; description: string }
): Promise<Course> => {
    const response: AxiosResponse<Course> = await axios.post(
        '/api/courses',
        course,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );
    return response.data;
};

// Add a new reflectometer to a course
export const addReflectometer = async (
    token: string,
    courseId: number,
    name: string
): Promise<Reflectometer> => {
    const response: AxiosResponse<Reflectometer> = await axios.post(
        `/api/reflectometer`,
        { name, course_id: courseId },
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );
    return response.data;
};

// Delete a reflectometer by ID
export const deleteReflectometer = async (
    token: string,
    reflectometerId: number
): Promise<void> => {
    await axios.delete(`/api/reflectometer/${reflectometerId}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
};
