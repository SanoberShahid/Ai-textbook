/// <reference types="@docusaurus/module-type-aliases" />
import clsx from 'clsx';
import Heading from '@theme/Heading';
import React from 'react';
import styles from './HomepageFeatures.module.css'; // Import the CSS module

import MountainSvg from '@site/static/img/undraw_docusaurus_mountain.svg';
import TreeSvg from '@site/static/img/undraw_docusaurus_tree.svg';
import ReactSvg from '@site/static/img/undraw_docusaurus_react.svg';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Comprehensive Chapters',
    Svg: MountainSvg,
    description: (
      <>
        Dive deep into the world of Physical AI and Humanoid Robotics with
        seven detailed chapters covering everything from fundamentals to advanced
        concepts.
      </>
    ),
  },
  {
    title: 'Interactive Quizzes',
    Svg: TreeSvg,
    description: (
      <>
        Test your knowledge at the end of each chapter with interactive quizzes
        to reinforce your learning and track your progress.
      </>
    ),
  },
  {
    title: 'Ask the Book',
    Svg: ReactSvg,
    description: (
      <>
        Have a question? Use our innovative "Ask the Book" feature to get
        answers directly from the textbook content itself, powered by AI.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

// Removed the inline 'styles' object as it's now imported from a CSS module
