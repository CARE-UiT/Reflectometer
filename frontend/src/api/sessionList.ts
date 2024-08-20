import axios, { AxiosResponse } from 'axios';

type UUID = string

export interface Curve {
    data: number[],
    session: UUID
}


export interface Session {
    id: UUID;
    name: string;
    curves: []
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

export const getSessions = async (token: string, courseId: number): Promise<Session[]> => {
    const response: AxiosResponse<Session[]> = await axios.get(`/api/courses/${courseId}/sessions`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    return response.data;
};

export const createSession = async (
    token: string,
    course: number,
    sessionName: string
): Promise<Session> => {
    const response: AxiosResponse<Session> = await axios.post(
        `/api/sessions`,
        {
            name: sessionName,
            course: course,
        },
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );
    return response.data;
};

export const deleteSession = async (token: string, sessionId: UUID): Promise<void> => {
    await axios.delete(`/api/sessions/${sessionId}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
};
